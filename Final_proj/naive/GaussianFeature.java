class GaussianFeature {
  private int m_featId;
  private int m_targetCount;
  private double[] m_avg;
  private double[] m_sigma;
  private double[] m_logSigma;

  public GaussianFeature(int featureId) {
    m_featId = featureId;
  }

  public void setTargetCount(int n) {
    m_targetCount = n;
  }

  // fit just a feature/attribute
  public void fit(NaiveRecord[] dat, final int[] freq) {
    // get average
    m_avg = new double[m_targetCount];
    for (int i = 0; i < dat.length; i++) {
      int y = dat[i].target;
      m_avg[y] += dat[i].num[m_featId];
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
    m_logSigma = new double[m_targetCount];
    for (int i = 0; i < m_targetCount; i++) {
      m_sigma[i] = Math.sqrt(m_sigma[i] / (freq[i]-1));
      m_logSigma[i] = Math.log(m_sigma[i]);
    }
    for (int i = 0; i < m_targetCount; i++) {
      NaiveTrain.printf("price range %d: %f %f\n", i, m_avg[i], m_sigma[i]);
    }
  }

  // calculate log(P(xi=v | y)), where v=feature, y=target
  // do you know what P(xi=v | y) is?
  public double getLogProb(double feature, int target) {
    // P(xi=v | y) = 1/sqrt(2*pi * sigma**2) * exp(-(v - avg)**2 / (2 * sigma**2))
    // where a**b means a^b
    // However, I decide to use natural logarithm because logarithm can prevent underflow
    // log P(xi=v | y) = -log(sigma) - (v - avg)**2 / (2 * sigma**2)
    double Z = (feature - m_avg[target]) / m_sigma[target];
    return -m_logSigma[target] - Z * Z / 2.0;
  }
}
