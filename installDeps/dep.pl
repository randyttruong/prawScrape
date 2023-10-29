#! /usr/bin/perl
use strict;
use warnings;


sub installDep() {
  print "Installing wheels... \n";
  system "pip install wheel";

  print "Installing mkl_fttl 1.3.3... \n";
  system "wget https://github.com/IntelPython/mkl_fft/archive/refs/tags/v1.3.3.zip";
  system "pip install ./v1.3.3.zip";
  print "Cleaning up mkl_fttl 1.3.3... \n";
  system "rm -rf ./v1.3.3.zip";
  print "Finished installing mkl_fttl 1.3.3... \n";

  sleep(2);
  system "clear";
  print "Installing mkl_random v1.2.3... \n";
  system "wget https://github.com/IntelPython/mkl_random/archive/refs/tags/v1.2.3.zip";
  system "pip install ./v1.2.3.zip";
  print "Cleaning up mkl_random v1.2.3... \n";
  system "rm -rf ./v1.2.3.zip";
  print "Finished installing mkl_random v1.2.3... \n";

  sleep(2);
  print "Installing mkl_service v2.4.0... \n";
  system "wget https://github.com/IntelPython/mkl-service/archive/refs/tags/v2.4.0.zip";
  system "pip install ./v2.4.0.zip";
  print "Cleaning up mkl_random v2.4.0... \n";
  system "rm -rf ./v2.4.0.zip";
  print "Finished installing mkl_random v2.4.0... \n";

  sleep(2);
  print "Installing intel-openmp 2021.4.0 \n";
  system "wget https://files.pythonhosted.org/packages/08/a0/eacf78b5d87cec6c6664d018b48d65051bf70bc43098e6fa589b17ae9f48/intel_openmp-2021.4.0-py2.py3-none-manylinux1_x86_64.whl";
  system "pip install intel_openmp-2021.4.0-py2.py3-none-manylinux1_x86_64.whl";
  print "Cleaning up intel-openmp 2021.4.0 \n";
  system "rm -rf intel_openmp-2021.4.0-py2.py3-none-manylinux1_x86_64.whl";
  print "Finished installing intel-openmp 2021.4.0 \n";

  sleep(2);
  print "Installing mkl 2021.4.0 \n";
  system "pip install mkl==2021.4.0";
  print "Finished installing mkl 2021.4.0 \n";





}

sub main() {
  installDep();
}

main();
