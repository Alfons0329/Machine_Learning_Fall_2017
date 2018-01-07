JC = javac
JFLAGS = 
CLASSES = \
	NaiveRecord.java \
	NaiveTrain.java \
	GaussianFeature.java \
	CategoryFeature.java \
	NaiveClassifier.java

.SUFFIXES: .java .class
.java.class:
	$(JC) $(JFLAGS) $*.java

default: classes

classes: $(CLASSES:.java=.class)

.PHONY: clean
clean:
	@rm -f *.class
