#include <tool/util_array.h>
#include <tool/util_tuple.h>
#include <scenegraph/container/indexarray.h>
#include <scenegraph/container/colorarray.h>
#include <boost/python.hpp>
#include <boost/python/make_constructor.hpp>

#include "../util/exception.h"
#include "../util/export_refcountptr.h"
#include "arrays_macro.h"

PGL_USING_NAMESPACE
TOOLS_USING_NAMESPACE

using namespace boost::python;

EXPORT_FUNCTION( c3a, Color3, Color3Array )
EXPORT_FUNCTION( c4a, Color4, Color4Array )
EXPORT_FUNCTION( i3a, Index3, Index3Array )
EXPORT_FUNCTION( i4a, Index4, Index4Array )
EXPORT_FUNCTION( inda,Index,  IndexArray )
EXPORT_FUNCTION( ra, real_t,  RealArray )

EXPORT_NUMPY( c3a, Color3, Color3Array, 0, 3, uchar_t )
EXPORT_NUMPY( c4a, Color4, Color4Array, 0, 4, uchar_t )
EXPORT_NUMPY( i3a, Index3, Index3Array, 0, 3, uint32_t )
EXPORT_NUMPY( i4a, Index4, Index4Array, 0, 4, uint32_t )
EXPORT_NUMPY( inda, Index, IndexArray, 0, 0, uint32_t )
EXPORT_NUMPY_1DIM( ra, real_t, RealArray, 0, real_t )

void export_arrays()
{
  EXPORT_ARRAY( c3a, Color3Array, "Color3Array([Index3(i,j,k),...])" )
    DEFINE_NUMPY( c3a );
  EXPORT_ARRAY( c4a, Color4Array, "Color4Array([Index4(i,j,k,l),...])" )
    DEFINE_NUMPY( c4a );

  EXPORT_ARRAY( i3a, Index3Array, "Index3Array([Index3(i,j,k),...])" )
    DEFINE_NUMPY( i3a );
  EXPORT_ARRAY( i4a, Index4Array, "Index4Array([Index4(i,j,k,l),...])" )
    DEFINE_NUMPY( i4a );
  EXPORT_ARRAY( inda,IndexArray,  "IndexArray([Index([i,j,..]),...])" )
    DEFINE_NUMPY( inda );
  EXPORT_ARRAY( ra, RealArray,  "IndexArray([a,b,...])" )
    DEFINE_NUMPY( ra );
}

