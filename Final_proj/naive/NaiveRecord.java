// stores a record

public class NaiveRecord {
  // continuous features
  public final double[] num;

  // discrete features
  public final String[] str;

  public NaiveRecord() {
    num = new double[4];
    str = new String[6];
  }

  // target
  public double price;
  // discrete target
  public int target;
}
