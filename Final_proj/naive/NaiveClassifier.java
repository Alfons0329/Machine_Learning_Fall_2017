class NaiveClassifier {
  // TODO: More continuous features
  private GaussianFeature[] continuousFeats;

  // TODO: More continuous features
  public void setContinuousFeatures(GaussianFeature ... feats) {
    continuousFeats = feats;
  }

  public void setTargetCount(int n) {
    for (int i = 0; i < continuousFeats.length; i++) {
      continuousFeats[i].setTargetCount(n);
    }
  }

  public void fit(NaiveRecord[] data) {
    for (int i = 0; i < continuousFeats.length; i++) {
      System.out.println("Fitting continuous feature "+i);
      continuousFeats[i].fit(data);
    }
  }
}
