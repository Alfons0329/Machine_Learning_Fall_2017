import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Map;
import java.util.TreeMap;
class MLIsHard {
  public static void main(String[] hard) {
    Map<String,Integer> a = new TreeMap<>();
    try {
      BufferedReader bi = new BufferedReader(new FileReader("train.csv"));
      String line;
      while ((line = bi.readLine()) != null) {
        String[] cols = line.split(",");
        String maker = cols[0];
        String model = cols[1];
        if (a.containsKey(model)) {
          a.put(model, a.get(model)+1);
        }
        else {
          a.put(model, 1);
        }
        int mileage = Integer.parseInt(cols[2]);
        int manufacture_year = Integer.parseInt(cols[3]);
        int engine_displ = Integer.parseInt(cols[4]);
        int engine_power = Integer.parseInt(cols[5]);
        String transmission = cols[6];
        int door = Integer.parseInt(cols[7]);
        int seat_count = Integer.parseInt(cols[8]);
        String fuel_type = cols[9];
        float price = Float.parseFloat(cols[10]);
      }
    }
    catch (FileNotFoundException qq) {
      System.out.println("Cannot find data");
    }
    catch (ArrayIndexOutOfBoundsException qq) {
      System.out.println("Format error");
    }
    catch (NumberFormatException qq) {
      System.out.println("Format error");
    }
    catch (IOException qq) {
      System.out.println("Read file error");
    }
    System.out.format("There are %d car models\n", a.size());
    int s1up = 0, s10up = 0, s100up = 0, s1000up = 0;
    for (Map.Entry<String,Integer> j : a.entrySet()) {
      int count = j.getValue();
      if (count >= 1000) s1000up++;
      else if (count >= 100) s100up++;
      else if (count >= 10) s10up++;
      else s1up++;
    }
    System.out.format("%d car models have 1~9 records\n", s1up);
    System.out.format("%d car models have 10~99 recodes\n", s10up);
    System.out.format("%d car models have 100~999 recodes\n", s100up);
    System.out.format("%d car models have 1000+ recodes\n", s1000up);
  }
}
