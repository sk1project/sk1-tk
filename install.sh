#!/bin/sh

# ---------------------------------------------------------------------------
# Check subroutine
# ---------------------------------------------------------------------------
check() {
if [ $? -ne 0 ]
then
	echo ""
	echo "======================================"
	echo " WARINIG!: "$CURRENT_STEP" "$OPERATION" is FAILED"
	echo " Try finding reason in stack trace."
	echo "======================================"
	exit
fi
}

# ---------------------------------------------------------------------------
# INSTALLATION PATH
# ---------------------------------------------------------------------------

INSTALL_PATH=~/sK1_Apps

# ---------------------------------------------------------------------------
# ENVIROMENT VARIABLES
# ---------------------------------------------------------------------------

RE_PREFIX=$INSTALL_PATH/sK1_RE
EPREFIX=$INSTALL_PATH/sK1
PREFIX=$EPREFIX

export LD_LIBRARY_PATH=$RE_PREFIX/lib
export PATH=$RE_PREFIX/bin:$PATH


# ---------------------------------------------------------------------------
# CLEAR POSSIBLE PREVIOUS sK1 INSTALLATION
# ---------------------------------------------------------------------------
echo "Clearing possible previous sK1 installation..."
rm -rf $EPREFIX

echo "Copying sK1 installation..."
cp -r src $INSTALL_PATH/sK1
rm -rf $PREFIX/modules; rm -rf $PREFIX/app/modules

echo "Removing .svn folders..."
for i in `find $EPREFIX |grep .svn`
do
	rm -rf $i
done

echo "Copying modules source code..."
cp -r src/modules build
rm -rf modules;mkdir modules

echo "Removing .svn folders..."
for i in `find build |grep .svn`
do
	rm -rf $i
done

exit
rm -rf build; mkdir build; cd build





rm -rf result
mkdir result
cd patches

echo
echo ---------------------------------------------------------------------------
echo Filter module Build
echo ---------------------------------------------------------------------------
echo

cd ../sketch_mod/Filter

sed 's/_MY_INSTALL_DIR_/'"$myEPREFIX"'/g' ../../patches/Filter/Makefile.pre.in |sed 's/_MY_INSTALL_PREFIX_/'"$myEPREFIX"'/g'> Makefile.pre.in

make -f Makefile.pre.in Makefile VERSION=2.4 installdir=$EPREFIX
make
#------------install-------------
cp streamfilter.so ../../result/streamfilter.so


echo
echo ---------------------------------------------------------------------------
echo pax-0.6.0 Build
echo ---------------------------------------------------------------------------
echo

cd ../pax-0.6.0
rm -rf *.o

sed 's/_MY_INSTALL_DIR_/'"$myEPREFIX"'/g' ../../patches/pax-0.6.0/Makefile.pre.in |sed 's/_MY_INSTALL_PREFIX_/'"$myEPREFIX"'/g'> Makefile.pre.in

myTCL_HEADERS=`echo $EPREFIX/include|sed 's/\//\\\ \//g'|sed 's/ \//\//g'`
myTCL_LIBS=`echo $EPREFIX/lib|sed 's/\//\\\ \//g'|sed 's/ \//\//g'`

sed 's/_MY_TCL_HEADERS_/'"$myTCL_HEADERS"'/g' ../../patches/pax-0.6.0/Setup.in |sed 's/_MY_TCL_LIBS_/'"$myTCL_LIBS"'/g'> Setup.in

make -f Makefile.pre.in Makefile VERSION=2.4 installdir=$EPREFIX
make
#------------install-------------
cp paxtkinter.so ../../result/paxtkinter.so
cp paxmodule.so ../../result/paxmodule.so


echo
echo ---------------------------------------------------------------------------
echo PS Modules
echo ---------------------------------------------------------------------------
echo

cd ../Modules

myIMAGING_HEADER=`echo $EPREFIX/include/PIL/libImaging|sed 's/\//\\\ \//g'|sed 's/ \//\//g'`

sed 's/_MY_IMAGING_HEADER_/'"$myIMAGING_HEADER"'/g' ../../patches/Modules/Setup.in > Setup.in
cat ../../patches/Modules/Setup.config > Setup.config

sed 's/_MY_INSTALL_DIR_/'"$myEPREFIX"'/g' ../../patches/Modules/Makefile.pre.in |sed 's/_MY_INSTALL_PREFIX_/'"$myEPREFIX"'/g'> Makefile.pre.in

make -f Makefile.pre.in Makefile VERSION=2.4 installdir=$EPREFIX
make
#------------install-------------
cp _sketchmodule.so ../../result/_sketchmodule.so
cp skreadmodule.so ../../result/skreadmodule.so
cp _type1module.so ../../result/_type1module.so
cp pstokenize.so ../../result/pstokenize.so

echo
echo ---------------------------------------------------------------------------
echo build completed!
echo ---------------------------------------------------------------------------

