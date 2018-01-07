// use Naive Bayes model to train
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Map;
import java.util.TreeMap;
import java.util.ArrayList;

class NaiveTrain {
  public static void puts(String str) {
    System.out.println(str);
  }

  public static void printf(String format, Object ...args) {
    System.out.format(format, args);
  }

  public static ArrayList<NaiveRecord> readDataset(String filename) {
    try {
      ArrayList<NaiveRecord> arr = new ArrayList<>();
      BufferedReader bi = new BufferedReader(new FileReader(filename));
      String line;
      while ((line = bi.readLine()) != null) {
        // split columns
        String[] cols = line.split(",");
        // get a record
        NaiveRecord rec = new NaiveRecord();
        rec.str[0] = cols[0]; // Maker
        rec.str[1] = cols[1]; // Model
        rec.num[0] = Integer.parseInt(cols[2]); // Mileage
        rec.num[1] = Integer.parseInt(cols[3]); // manufacture_year
        rec.num[2] = Integer.parseInt(cols[4]); // Engine_displ
        rec.num[3] = Integer.parseInt(cols[5]); // Engine_power
        rec.str[2] = cols[6]; // Transmission
        rec.str[3] = cols[7]; // Door
        rec.str[4] = cols[8]; // seat count
        rec.str[5] = cols[9]; // Fuel_type
        rec.price = Float.parseFloat(cols[10]);
        arr.add(rec);
      }
      return arr;
    }
    catch (FileNotFoundException qq) {
      puts("Cannot find data");
      return null;
    }
    catch (ArrayIndexOutOfBoundsException qq) {
      puts("Format error");
      return null;
    }
    catch (NumberFormatException qq) {
      puts("Format error");
      return null;
    }
    catch (IOException qq) {
      puts("Read file error");
      return null;
    }
  }

  static void TellMePriceRange(NaiveRecord[] dat) {
    int[] range = new int[8];
    for (int i = 0; i < dat.length; i++) {
      double $$ = dat[i].price;
      int y;
      if ($$ > 1_000_000) y = 7;
      else if ($$ > 100_000) y = 6;
      else if ($$ > 10_000) y = 5;
      else if ($$ > 1_000) y = 4;
      else if ($$ > 100) y = 3;
      else if ($$ > 10) y = 2;
      else if ($$ > 1) y = 1;
      else y = 0;
      dat[i].target = y;
      range[y]++;
    }
    printf("less than 1: %d\n", range[0]);
    printf("1 ~ 10: %d\n", range[1]);
    printf("10 ~ 100: %d\n", range[2]);
    printf("100 ~ 1,000: %d\n", range[3]);
    printf("1,000 ~ 10,000: %d\n", range[4]);
    printf("10,000 ~ 100,000: %d\n", range[5]);
    printf("100,000 ~ 1,000,000: %d\n", range[6]);
    printf("more than 1,000,000: %d\n", range[7]);
  }

  public static void main(String[] args) {
    if (args.length < 2) {
      puts("Usage: java NaiveRead <train data.csv> <test data.csv>");
      return ;
    }
    String trainFile = args[0], testFile = args[1];
    puts("Reading training data");
    ArrayList<NaiveRecord> arrList = readDataset(trainFile);
    if (null == arrList) return ;
    NaiveRecord[] trainData = new NaiveRecord[arrList.size()];
    arrList.toArray(trainData);
    puts("Discretizing price");
    TellMePriceRange(trainData);

    puts("Training");
    NaiveClassifier bayes = new NaiveClassifier();
    bayes.setContinuousFeatures(
      new GaussianFeature(0), // Mileage
      new GaussianFeature(1), // manufacture_year
      new GaussianFeature(2), // Engine_displ
      new GaussianFeature(3) // Engine_power
    );
    bayes.setDiscreteFeatures(
      new CategoryFeature(2), // Transmission
      new CategoryFeature(3), // Door
      new CategoryFeature(4), // seat count
      new CategoryFeature(5) // Fuel_type
    );
    bayes.setTargetCount(8);
    bayes.fit(trainData);

    puts("Reading testing data");
    arrList = readDataset(testFile);
    if (null == arrList) return ;
    NaiveRecord[] testData = new NaiveRecord[arrList.size()];
    arrList.toArray(testData);
    puts("Discretizing price");
    TellMePriceRange(testData);

    puts("Testing");
    bayes.predict(testData);
  }
}
