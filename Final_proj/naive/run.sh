javac -version || {
  echo "Cannot run Java compiler. Please install Java JDK or OpenJDK"
  echo "you can try sudo apt-get install openjdk-8-jdk"
  exit
}
echo compile...
javac *.java
echo run...
java NaiveTrain ../train.csv ../test.csv
