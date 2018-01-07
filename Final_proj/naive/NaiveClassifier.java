class NaiveClassifier {
  // my classmate says I only need Gaussian Naive Bayes
  private GaussianFeature[] continuousFeats;
  private CategoryFeature[] discreteFeats;
  private int targetCount;
  private int[] freq; // freq[i] = occurrence of target i
  private double[] logProb;
  // logProb[i] = Math.log(P(y=i)) = Math.log(freq[i] / data size)
  // = Math.log(freq[i]) - Math.log(data size)
  // however, data size is a constant, so I can ignore that term

  public NaiveClassifier() {
    continuousFeats = new GaussianFeature[0];
    discreteFeats = new CategoryFeature[0];
  }

  public void setContinuousFeatures(GaussianFeature ... feats) {
    continuousFeats = feats;
  }

  public void setDiscreteFeatures(CategoryFeature ... feats) {
    discreteFeats = feats;
  }

  public void setTargetCount(int n) {
    for (int i = 0; i < continuousFeats.length; i++) {
      continuousFeats[i].setTargetCount(n);
    }
    for (int i = 0; i < discreteFeats.length; i++) {
      discreteFeats[i].setTargetCount(n);
    }
    targetCount = n;
  }

  public void fit(NaiveRecord[] data) {
    freq = new int[targetCount];
    for (int i = 0; i < data.length; i++) {
      freq[data[i].target]++;
    }

    logProb = new double[targetCount];
    for (int i = 0; i < targetCount; i++) {
      logProb[i] = Math.log(freq[i]);
    }

    for (int i = 0; i < continuousFeats.length; i++) {
      System.out.println("Fitting continuous feature " + continuousFeats[i].getFeatId());
      continuousFeats[i].fit(data, freq);
    }
    for (int i = 0; i < discreteFeats.length; i++) {
      System.out.println("Fitting discrete feature " + discreteFeats[i].getFeatId());
      discreteFeats[i].fit(data, freq);
    }
  }

  public int[] predict(NaiveRecord[] data) {
    int[] result = new int[data.length];
    int yes = 0;
    for (int i = 0; i < data.length; i++) {
      int best = 0;
      double maxLogP = -1.0e30;
      for (int y = 0; y < targetCount; y++) {
        double logP = logProb[y];
        for (int j = 0; j < continuousFeats.length; j++) {
          logP += continuousFeats[j].getLogProb(data[i], y);
        }
        for (int j = 0; j < discreteFeats.length; j++) {
          logP += discreteFeats[j].getLogProb(data[i], y);
        }
        if (logP > maxLogP) {
          best = y;
          maxLogP = logP;
        }
      }
      result[i] = best;
      if (result[i] == data[i].target) yes++;
    }
    NaiveTrain.printf("Accuracy: %f\n", (double)yes/data.length);
    return result;
  }
}
