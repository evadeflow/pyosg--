import os
import sys
import cmake
from pyplusplus import module_builder
#from pyplusplus.module_builder import call_policies

MODULE_NAME = 'osg'

# Python string template used to declare a C++ function template for helper
# functions used to access the x, y, z, etc. components of a vector from
# python.  (The goal is to expose the x(), y(), z() member functions used by
# the OSG vector classes as python properties named 'x', 'y', 'z', etc.)
#
VEC_XYZW_RGBA_DECL = """
// Retrieve the '%(VarName)s' component of a vector
template <typename T>
static typename T::value_type Vec_%(VarName)s_getter(T const& self)
{
    return self.%(VarName)s();
}

// Set the '%(VarName)s' component of a vector
template <typename T>
static void Vec_%(VarName)s_setter(T& self, typename T::value_type value)
{
    self.%(VarName)s() = value;
}
"""

# Python string template containing a snippet of Boost.Python code to expose
# the x(), y(), z(), etc. members of the various vector classes as properties.
#
VEC_XYZRGB_REG = """
add_property(
    "%(VarName)s"
    , &Vec_%(VarName)s_getter<osg::%(ClsName)s>
    , &Vec_%(VarName)s_setter<osg::%(ClsName)s>
    , "%(VarName)s component of the vector")
"""


# Python string containing definitions of some function templates needed to
# make vectors iterable/indexable...
# 
VEC_GETSET_ITEM_DECL = """
template<typename T>
static int Vec_len(T const& self)
{
    return self.num_components;
}

template<typename T>
static typename T::value_type Vec_getitem(T const& self, int index)
{
    if (index < 0 || index > self.num_components - 1)
    {
        throw std::out_of_range("vector index out of range");
    }

    return self._v[index];
}

template<typename T>
static void Vec_setitem(T& self, int index, typename T::value_type value)
{
    if (index < 0 || index > self.num_components - 1)
    {
        throw std::out_of_range("vector index out of range");
    }

    self._v[index] = value;
}
"""


def getParentClasses(funcList):
  """ Given a set of member functions, return a list of the classes that
      contain them, removing duplicates
  """
  classes = {}
  for func in funcList:
      classes[func.parent.name] = 1
  return classes.keys()

cache_header = os.path.join(cmake.abspath(sys.argv[0]), 'osg.pypp.h')
gccxml_cache = cmake.create_gccxml_cache(cache_header)

mb = module_builder.module_builder_t(
        [gccxml_cache]
        , gccxml_path=cmake.GCCXML
        , include_paths=[cmake.OSG_INCLUDE_DIR]
        , define_symbols=cmake.GCCXML_DEFINES
        , cflags='--gccxml-compiler ' + cmake.GCCXML_COMPILER)

# Make all ctors explicit
mb.constructors().allow_implicit_conversion = False

mb.classes().always_expose_using_scope = True

# Exclude everything from the global namespace
global_ns = mb.global_ns
global_ns.exclude()

# Include everything in namespace 'osg' by default
main_ns = global_ns.namespace('osg')
main_ns.include()

# Exclude all member functions (of all classes!) named 'ptr'
mb.member_functions('ptr').exclude()

# Declare templated getitem/setitem helper funcs used by all vector classes
mb.add_declaration_code(VEC_GETSET_ITEM_DECL)

# Special handling for all 'Vec' classes:
for cls in mb.classes(lambda cls: cls.name.startswith('Vec')):

    # Don't expose operator[]() - it's inappropriate in python
    cls.operators('[]').exclude()

    # Don't allow direct access to the underlying array
    cls.variables('_v').exclude()

    # Register functions to get container-like behavior in python
    # (takes the place of operator[](), does range-checking, permits iteration...)
    cname = cls.name
    cls.add_registration_code('def("__len__", &Vec_len<osg::%s>)' % cname)
    cls.add_registration_code('def("__getitem__", &Vec_getitem<osg::%s>)' % cname)
    cls.add_registration_code('def("__setitem__", &Vec_setitem<osg::%s>)' % cname)


# Special handling for Vec member functions that return a reference
for varName in ('x', 'y', 'z', 'w', 'r', 'g', 'b', 'a'):

    # Declare templated helper functions to allow mapping to a property
    mb.add_declaration_code(VEC_XYZW_RGBA_DECL % dict(VarName=varName))

    # Hide any member function (in *any* class) matching 'varName'
    xyzwRgbaFuncs = mb.member_functions(varName)
    xyzwRgbaFuncs.exclude()

    # For each class that contained a 'problem' accessor, we need to register
    # a property with the same name (e.g., 'r') and point the getter and setter
    # for it at the templated utility funcs we injected above
    classes = getParentClasses(xyzwRgbaFuncs)
    for cls in classes:
        regcode = VEC_XYZRGB_REG % dict(VarName=varName, ClsName=cls)
        mb.class_(cls).add_registration_code(regcode)


# Give the module a name (will be used when doing 'import blah' in python)
mb.build_code_creator(module_name=MODULE_NAME)

# Here's how you'd include a license statement at the top of each file
mb.code_creator.license = '//Boost Software License(http://boost.org/more/license_info.html)'

# Write code to disk
bindings_file = MODULE_NAME + '_bindings.cpp'
mb.write_module(os.path.join(os.path.abspath('.'), bindings_file))
