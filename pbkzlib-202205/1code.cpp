#include <lattice/pbkz.hpp>
#include <fstream>

int main(){
    ofstream outfile;
    outfile.open("pbkz_data.txt");

    int dim = 58; // Dimension of challenge instance
    int trial = 1;  //生成trial个挑战格
    int start_beta = 20;
    int final_beta = 50;
    int beta_add = 3;
    int vl = VL1; // Display small amount of information
    std::string stringoption = ""; // No specific options
    mat_ZZ U; U.SetDims(dim, dim);

    for (int i = 0; i < trial;i++){
        int seed = rand() % 10000;

        for (int beta = start_beta; beta < final_beta; beta = beta_add+beta){
            LatticeBasis<long double> lB; // Gram-Schmidt coefficients are computed in long double precision
            lB = svpc::getbasis(dim, seed);  // Call the generator
            BigLLL(lB.L, 0, 0.999, VL1);     // Call LLL subroutine having huge elements
            lB.updateGSBasis();              // Before output, need to update GS basis
            ProgressiveBKZ<long double>(lB, &U, beta, vl, stringoption);

            double gh = LengthOf(lB.L[0]) / LatticeGH(lB);
            outfile << "dim =" << dim << "; seed =" << seed << "; final beta =" << beta << "; |b1|=" << gh << "*GH" << endl;
            outfile << "first vector = " << lB.L[0] << endl;
            outfile << endl;
        }
    }
    outfile.close();

    return 0;
}

/*
    cout << "first vector = " << dB.L[0] << endl;

    cout << "|b*i|: ";
    dB.gs.displayc();

    double gh = LatticeGH(dB);
    cout << "GaussianHeuristic(L)=" << gh << endl;

        cout << "|b1|=" << LengthOf(B.L[0]) / LatticeGH(B) << endl;

        cout << "found vector=" << lB.L[0] << endl;
    cout << "|b1|=" << LengthOf(lB.L[0]) / gh << "*GH" << endl;



    cout << "find vector: " << B.L[0] << endl;
    cout << "Length=" << B.gs.c[1] << "=" << B.gs.c[1]/LatticeGH(B) << "*GH(L)" << endl;

    */