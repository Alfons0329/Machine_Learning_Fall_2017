import java.util.Map;
import java.util.HashMap;

class CategoryFeature {
  private int m_featId;
  private int m_targetCount;
  private double m_alpha; // smoothing
  private HashMap<String, int[]> m_count;
  private HashMap<String, double[]> m_logProb;

  public CategoryFeature(int featureId) {
    m_featId = featureId;
    m_alpha = 1.0; // laplace smoothing
  }

  public void setTargetCount(int n) {
    m_targetCount = n;
  }

  public int getFeatId() {
    return m_featId;
  }

  // fit just a feature/attribute
  public void fit(NaiveRecord[] dat, final int[] freq) {
    m_count = new HashMap<>();
    // count feature
    for (int i = 0; i < dat.length; i++) {
      String x = dat[i].str[m_featId];
      int y = dat[i].target;
      if (m_count.containsKey(x)) {
        m_count.get(x)[y]++;
      }
      else {
        int[] countArr = new int[m_targetCount];
        countArr[y]++;
        m_count.put(x, countArr);
      }
    }

    int nFeats = m_count.size();
    // calculate probability
    double[] logY = new double[m_targetCount];
    for (int i = 0; i < m_targetCount; i++) {
      logY[i] = Math.log(freq[i] + m_alpha * nFeats);
    }
    m_logProb = new HashMap<>();
    // for each feature...
    for (Map.Entry<String,int[]> p : m_count.entrySet()) {
      int[] nxy = p.getValue();
      double[] logP = new double[m_targetCount];
      for (int i = 0; i < m_targetCount; i++) {
        logP[i] = Math.log(nxy[i] + m_alpha) - logY[i];
      }
      m_logProb.put(p.getKey(), logP);
      // show histogram
      if (nFeats < 50) {
        System.out.print(p.getKey());
        for (int i = 0; i < m_targetCount; i++) {
          NaiveTrain.printf(" %d", nxy[i]);
        }
        NaiveTrain.puts("");
      }
    }
  }

  // calculate log(P(xi=v | y)), where v=feature, y=target
  // do you know what P(xi=v | y) is?
  public double getLogProb(NaiveRecord dat, int target) {
    // P(xi=v | y) = N(y and xi=v) / N(y)
    String feature = dat.str[m_featId];
    if (m_logProb.containsKey(feature)) {
      return m_logProb.get(feature)[target];
    }
    else {
      // missing feature
      return 0.0;
    }
  }
}
