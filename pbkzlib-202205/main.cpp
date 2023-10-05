/*
   progressive BKZ library by NICT security fundemental lab.
 */

#pragma GCC diagnostic ignored "-Wunknown-attributes"

//comment out when publishing
//#define __develop

#include <lattice/pbkz.hpp>

#include <boost/version.hpp>
#include <boost/lexical_cast.hpp>

#include <boost/multiprecision/mpfr.hpp>
using namespace boost::multiprecision;

#include <boost/functional/hash.hpp>

#include "lattice/bkztest.cpp"

#include <boost/math/special_functions/binomial.hpp>
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/multiprecision/cpp_dec_float.hpp>


int main(int argc, char** argv) {
	bkztest();   
}
