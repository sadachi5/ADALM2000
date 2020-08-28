#!/bin/bash
cd swig
LAN=csharp
make check-${LAN}-test-suite | tee make_${LAN}.out
LAN=java
make check-${LAN}-test-suite | tee make_${LAN}.out
LAN=python
make check-${LAN}-test-suite | tee make_${LAN}.out
LAN=perl5
make check-${LAN}-test-suite | tee make_${LAN}.out
LAN=ruby
make check-${LAN}-test-suite | tee make_${LAN}.out
LAN=d
make check-${LAN}-test-suite | tee make_${LAN}.out
LAN=octave
make check-${LAN}-test-suite | tee make_${LAN}.out
LAN=tcl
make check-${LAN}-test-suite | tee make_${LAN}.out
cd ../
