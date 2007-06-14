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

echo
echo ---------------------------------------------------------------------------
echo sK1 build starts...
echo ---------------------------------------------------------------------------
echo

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

myEPREFIX=`echo $RE_PREFIX|sed 's/\//\\\ \//g'|sed 's/ \//\//g'`

# ---------------------------------------------------------------------------
# PREPARE sK1 INSTALLATION
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
rm -rf build;cp -r src/modules build
rm -rf modules;mkdir modules

echo "Removing .svn folders..."
for i in `find build |grep .svn`
do
	rm -rf $i
done


# ---------------------------------------------------------------------------
# MODULES BUILD
# ---------------------------------------------------------------------------
cd build

echo
echo ---------------------------------------------------------------------------
echo Filter module build
echo ---------------------------------------------------------------------------
echo
CURRENT_STEP="Filter module"
cd Filter

sed 's/_MY_INSTALL_DIR_/'"$myEPREFIX"'/g' Makefile.pre.in |sed 's/_MY_INSTALL_PREFIX_/'"$myEPREFIX"'/g'> Makefile.pre; rm -f Makefile.pre.in;mv Makefile.pre Makefile.pre.in

OPERATION="make -f"
make -f Makefile.pre.in Makefile VERSION=2.4 installdir=$RE_PREFIX
check
OPERATION="make"
make
check
#------------install-------------
cp streamfilter.so ../../modules/streamfilter.so

echo
echo ---------------------------------------------------------------------------
echo pax-0.6.0 Build
echo ---------------------------------------------------------------------------
echo
CURRENT_STEP="pax-0.6.0 module"
cd ../pax-0.6.0
rm -rf *.o

sed 's/_MY_INSTALL_DIR_/'"$myEPREFIX"'/g' Makefile.pre.in |sed 's/_MY_INSTALL_PREFIX_/'"$myEPREFIX"'/g'> Makefile.pre; rm -f Makefile.pre.in;mv Makefile.pre Makefile.pre.in

myTCL_HEADERS=`echo $RE_PREFIX/include|sed 's/\//\\\ \//g'|sed 's/ \//\//g'`
myTCL_LIBS=`echo $RE_PREFIX/lib|sed 's/\//\\\ \//g'|sed 's/ \//\//g'`

sed 's/_MY_TCL_HEADERS_/'"$myTCL_HEADERS"'/g' Setup.in |sed 's/_MY_TCL_LIBS_/'"$myTCL_LIBS"'/g'> Setup.in.pre; rm -f Setup.in; mv Setup.in.pre Setup.in

OPERATION="make -f"
make -f Makefile.pre.in Makefile VERSION=2.4 installdir=$RE_PREFIX
check
OPERATION="make"
make
check
#------------install-------------
cp paxtkinter.so ../../modules/paxtkinter.so
cp paxmodule.so ../../modules/paxmodule.so


echo
echo ---------------------------------------------------------------------------
echo PS Modules
echo ---------------------------------------------------------------------------
echo
CURRENT_STEP="Modules"

cd ../Modules

myIMAGING_HEADER=`echo $RE_PREFIX/include/PIL|sed 's/\//\\\ \//g'|sed 's/ \//\//g'`

sed 's/_MY_TCL_HEADERS_/'"$myTCL_HEADERS"'/g' Setup.in |sed 's/_MY_TCL_LIBS_/'"$myTCL_LIBS"'/g' |sed 's/_MY_IMAGING_HEADER_/'"$myIMAGING_HEADER"'/g' > Setup.in.pre; rm -f Setup.in; mv Setup.in.pre Setup.in

# cat ../../patches/Modules/Setup.config > Setup.config

sed 's/_MY_INSTALL_DIR_/'"$myEPREFIX"'/g' Makefile.pre.in |sed 's/_MY_INSTALL_PREFIX_/'"$myEPREFIX"'/g'> Makefile.pre; rm -f Makefile.pre.in;mv Makefile.pre Makefile.pre.in

OPERATION="make -f"
make -f Makefile.pre.in Makefile VERSION=2.4 installdir=$RE_PREFIX
check
OPERATION="make"
make
check

#------------install-------------
cp _sketchmodule.so ../../modules/_sketchmodule.so
cp skreadmodule.so ../../modules/skreadmodule.so
cp _type1module.so ../../modules/_type1module.so
cp pstokenize.so ../../modules/pstokenize.so

cd ..;cd ..
mv modules $PREFIX/app/modules;rm -rf build
START=$PREFIX/sk1.sh

echo "#!/bin/sh">>$START
echo "#This script is automatically created by sK1 build">>$START
echo "">>$START
echo "export LD_LIBRARY_PATH="$LD_LIBRARY_PATH>>$START
echo "export PATH=$RE_PREFIX/bin:\$PATH">>$START
echo "">>$START
echo "echo \"sK1 starts...\"">>$START
echo "python $PREFIX/main.py \$1">>$START

chmod +x $START

START=$PREFIX/uniconvertor.sh

echo "#!/bin/sh">>$START
echo "#This script is automatically created by sK1 build">>$START
echo "">>$START
echo "export LD_LIBRARY_PATH="$LD_LIBRARY_PATH>>$START
echo "export PATH=$RE_PREFIX/bin:\$PATH">>$START
echo "">>$START
echo "python $PREFIX/conv.py \$1 \$2">>$START

chmod +x $START

echo
echo ---------------------------------------------------------------------------
echo sK1 build completed! To launch sK1 use $EPREFIX/sk1.sh script
echo ---------------------------------------------------------------------------
