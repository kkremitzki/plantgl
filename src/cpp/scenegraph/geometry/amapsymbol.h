/* -*-c++-*-
 *  ----------------------------------------------------------------------------
 *
 *       AMAPmod: Exploring and Modeling Plant Architecture
 *
 *       Copyright 1995-2000 UMR Cirad/Inra Modelisation des Plantes
 *
 *       File author(s): C. Nouguier & F. Boudon (frederic.boudon@cirad.fr) nouguier
 *
 *       $Source$
 *       $Id$
 *
 *       Forum for AMAPmod developers    : amldevlp@cirad.fr
 *
 *  ----------------------------------------------------------------------------
 *
 *                      GNU General Public Licence
 *
 *       This program is free software; you can redistribute it and/or
 *       modify it under the terms of the GNU General Public License as
 *       published by the Free Software Foundation; either version 2 of
 *       the License, or (at your option) any later version.
 *
 *       This program is distributed in the hope that it will be useful,
 *       but WITHOUT ANY WARRANTY; without even the implied warranty of
 *       MERCHANTABILITY or FITNESS For A PARTICULAR PURPOSE. See the
 *       GNU General Public License for more details.
 *
 *       You should have received a copy of the GNU General Public
 *       License along with this program; see the file COPYING. If not,
 *       write to the Free Software Foundation, Inc., 59
 *       Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 *
 *  ----------------------------------------------------------------------------
 */

/*! \file geom_amapsymbol.h
    \brief Definition of the geometry class AmapSymbol.
*/



#ifndef __geom_amapsymbol_h__
#define __geom_amapsymbol_h__

/* ----------------------------------------------------------------------- */

#include "geom_faceset.h"

/* ----------------------------------------------------------------------- */

TOOLS_BEGIN_NAMESPACE
class beifstream;
TOOLS_END_NAMESPACE

/* ----------------------------------------------------------------------- */

GEOM_BEGIN_NAMESPACE

/* ----------------------------------------------------------------------- */

/**
   \class AmapSymbol
   \brief An Amap Symbol
*/

class GEOM_API AmapSymbol : public FaceSet
{

public:

  /// A structure which helps to build a AmapSymbol when parsing.
  struct Builder : public FaceSet::Builder {

    /// A pointer to the \b FileName field.
    std::string * FileName;

    /// Constructor.
    Builder( );

    /// Detructor.
    virtual ~Builder( );

    virtual SceneObjectPtr build( ) const;

    virtual void destroy( );

    virtual bool isValid( ) const;

  };

  /// Default Constructor. Build object is invalid.
  AmapSymbol();

  /** Constructs an AmapSymbol with the datas stored in the file specified
      by \e fileName. The \e solid flag specifies whether the AmapSymbol is
      closed.
      \pre
      - \e fileName must exist and must be readable. */
  AmapSymbol( const std::string& fileName, bool solid=FaceSet::DEFAULT_SOLID );

  /** Constructs an AmapSymbol with the FaceSet \e faceSet.
      \pre
      - \e faceSet must be non null and valid. */
  AmapSymbol( const FaceSetPtr& faceSet );

  /// Destructor
  virtual ~AmapSymbol( );

  virtual bool apply( Action& action );

  /// Returns \b FileName value.
  const std::string& getFileName( ) const ;

  /// Returns \b FileName field.
  std::string& getFileName( ) ;

  virtual bool isValid( ) const;


  /** Fill \e this with the datas stored in the file specified
      by \e fileName. The \e solid flag specifies whether the AmapSymbol is
      closed.
      \pre
      - \e fileName must exist and must be readable. */
  bool readFile(const std::string& filename);

  virtual TOOLS(bofstream)& write( TOOLS(bofstream)& stream ) const;

  /** Read the datas stored in the file specified
      in stream. */
  virtual TOOLS(beifstream)& read( TOOLS(beifstream)& stream );

  const TOOLS(Vector3)& getTexCoord3At( uint32_t i, uint32_t j ) const;
  
  TOOLS(Vector3)& getTexCoord3At( uint32_t i, uint32_t j );

  const Point3ArrayPtr& getTexCoord3List() const{
	return __texCoord3List; }

  Point3ArrayPtr& getTexCoord3List() {
	return __texCoord3List; }

  bool hasTexCoord3List() const {
	return __texCoord3List.isValid(); }

  protected:

  /// The \b FileName field.
  std::string __fileName;

  Point3ArrayPtr __texCoord3List;
};

/// AmapSymbol Pointer
typedef RCPtr<AmapSymbol> AmapSymbolPtr;


/* ----------------------------------------------------------------------- */

// __geom_amapsymbol_h__
/* ----------------------------------------------------------------------- */

GEOM_END_NAMESPACE

/* ----------------------------------------------------------------------- */
#endif
