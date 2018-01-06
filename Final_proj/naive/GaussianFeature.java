class GaussianFeature {
  private int m_featId;
  private int m_targetCount;
  private double[] m_avg;
  private double[] m_sigma;

  public GaussianFeature(int featureId) {
    m_featId = featureId;
  }

  public void setTargetCount(int n) {
    m_targetCount = n;
  }

  // fit just a feature/attribute
  public void fit(NaiveRecord[] dat) {
    // get average
    int[] freq = new int[m_targetCount];
    m_avg = new double[m_targetCount];
    for (int i = 0; i < dat.length; i++) {
      int y = dat[i].target;
      m_avg[y] += dat[i].num[m_featId];
      freq[y]++;
    }
    for (int i = 0; i < m_targetCount; i++) {
      m_avg[i] /= freq[i];
    }

    // calculate standard deviation
    m_sigma = new double[m_targetCount];
    for (int i = 0; i < dat.length; i++) {
      int y = dat[i].target;
      double d = dat[i].num[m_featId] - m_avg[y];
      m_sigma[y] += d * d;
    }
    for (int i = 0; i < m_targetCount; i++) {
      m_sigma[i] = Math.sqrt(m_sigma[i] / freq[i]);
    }
    for (int i = 0; i < m_targetCount; i++) {
      NaiveTrain.printf("price range %d: %f %f\n", i, m_avg[i], m_sigma[i]);
    }
  }
}
