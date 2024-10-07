#!/bin/bash

# Get a temporary directory
tmpdir=$(mktemp -d)

javac -d $tmpdir box/*.java
jar cvfe ../dist/jar-of-java.jar box.MainClass -C $tmpdir .

rm -r $tmpdir