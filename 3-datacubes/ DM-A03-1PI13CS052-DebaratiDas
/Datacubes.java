
import weka.core.Instances;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

import java.util.HashMap;
import java.util.Hashtable;
import java.util.Map;

import weka.core.Attribute;
import weka.core.converters.ConverterUtils.DataSource;
import weka.core.AttributeStats;
import weka.core.Instance;
import weka.experiment.Stats;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Discretize;

// Data Mining - Data Cubes Assignment
// Done by Debarati Das  : 1PI13CS052

public class Datacubes {

	public static void main(String args[]) throws IOException {
		BufferedWriter w;

		w = new BufferedWriter(new FileWriter("output.txt"));

		String filename = "bank-data.csv";
		DataSource source;
		try {
			// Create new data source
			source = new DataSource(filename);
			// Read instances from the CSV file

			Instances instances = source.getDataSet();

			// Delete the attributes other than those needed
			// 4 is repeated because you deleted the fourth item in case 1 and
			// every other time shifted to the left by one
			instances.deleteAttributeAt(0);
			instances.deleteAttributeAt(4);
			instances.deleteAttributeAt(4);
			instances.deleteAttributeAt(4);
			instances.deleteAttributeAt(4);
			instances.deleteAttributeAt(4);
			instances.deleteAttributeAt(4);
			instances.deleteAttributeAt(4);

			// Print header and instances of the dataset
			// System.out.println("\nDataset:\n");
			// System.out.println(instances);

			// Using unsupervised Discretize

			Discretize filter = new Discretize();
			filter.setAttributeIndices("1"); // this makes sure only age
												// attribute is discretized

			// Set number of bins
			filter.setBins(3);
			filter.setInputFormat(instances);

			Instances output = Filter.useFilter(instances, filter);

			double[] cutPoints = filter.getCutPoints(0); // get cutpoints of age
															// = 0th attribute
			// print out the cutpoints and the frequencies in each bin
			System.out.println("Cut points for the three bins are :");
			for (int i = 0; i < cutPoints.length; i++) {
				System.out.println(cutPoints[i]);
			}

			double income[] = instances.attributeToDoubleArray(3);
			// Renaming the attributes !

			output.renameAttributeValue(0, 0, "YOUNG");

			output.renameAttributeValue(0, 1, "MIDDLE");

			output.renameAttributeValue(0, 2, "OLD");

			System.out.println("\nDataset after modification:\n");
			System.out.println(output);
			Scanner in = new Scanner(System.in);

			w.write(output.toString());
			w.newLine();
			w.flush();
			w.close();

			// invoke Datacubes function now.

			int n = 0;
			do {
				System.out.println("Enter n for the Datacubes ");
				n = in.nextInt();
				if (n == 0)
				{
					System.out.println("Datacubes(0)");
					Datacubes_0(0, income);
				}

				else if (n == 1) {
					System.out.println("Datacubes(1)");
					System.out.println("WRT AGE");
					System.out.println("_____________________________________________________________________________________________________");

					datacubes(1, output, 0, income);
					System.out.println("WRT SEX");
					System.out.println("_____________________________________________________________________________________________________");

					datacubes(1, output, 1, income);
					System.out.println("WRT REGION");
					System.out.println("_____________________________________________________________________________________________________");

					datacubes(1, output, 2, income);
				} else if (n==2) {
					System.out.println("Datacubes(2)");
					System.out.println("WRT AGE/SEX");
					System.out.println("_____________________________________________________________________________________________________");

					datacubes_2_or_3D(1, output, new int[] {0, 1}, income);
					System.out.println("WRT SEX/REGION");
					System.out.println("_____________________________________________________________________________________________________");

					datacubes_2_or_3D(1, output, new int[] {1, 2}, income);
					System.out.println("WRT AGE/REGION");
					System.out.println("_____________________________________________________________________________________________________");

					datacubes_2_or_3D(1, output, new int[] {0, 2}, income); 
				} else if (n==3) {
					System.out.println("Datacubes(3)");
					System.out.println("WRT AGE/SEX/REGION");
					System.out.println("_____________________________________________________________________________________________________");

					datacubes_2_or_3D(1, output, new int[] {0, 1, 2}, income);
				}
				 else
					 break;
				

			} while (n != 5);

		} catch (Exception e) {
			e.printStackTrace();
		}

	}

	static void Datacubes_0(int index, double[] income) {
		int count = income.length;
		double sum = 0;
		for (int i = 0; i < income.length; i++) {
			sum += income[i];
		}
		double average = sum / count;
		average = (double) Math.round(average * 1000d) / 1000d;

		System.out.printf("%-10s %-10s %-20s\n", "All", "Count", "Average income");
		System.out.printf("%-10s %-10s %-20s\n", "  ", count, average);

	}

	static void datacubes(int index, Instances output, int dimIndex, double[] income) {
		Map<String, Integer> dictionary_agerange = new HashMap();
		Map<String, Double> dictionary_tot_income = new HashMap();
		//Map<String, Double> dictionary_tot_count = new HashMap();
		int ctr = 0;

		// age : gives ages
		// income: gives income
		
		int ct = 0;
		for (int i = 0; i < output.numInstances(); i++) {
			Instance record = output.instance(i);
			String age_range = record.stringValue(dimIndex);

			if (dictionary_agerange.containsKey(age_range)) {
				ct = (Integer) dictionary_agerange.get(age_range); 
				dictionary_agerange.put(age_range, ct+1);
				dictionary_tot_income.put(age_range, income[i] + dictionary_tot_income.get(age_range));
			} else {
				dictionary_agerange.put(age_range, 1);
				dictionary_tot_income.put(age_range, income[i]);
			}
		}

		for(String age_range: dictionary_agerange.keySet()) {
			System.out.printf("\n%-30s\t%f\n", age_range, dictionary_tot_income.get(age_range)/ dictionary_agerange.get(age_range));
			System.out.printf("\n%-30s\t%s\n", "COUNT(category)", dictionary_agerange.get(age_range));
		}

	}
	
	static void datacubes_2_or_3D(int index, Instances output, int dim[], double[] income) {
		Map<String, Integer> dictionary_agerange = new HashMap();
		Map<String, Double> dictionary_tot_income = new HashMap();
		int ctr = 0;

		
		
		int ct = 0;
		for (int i = 0; i < output.numInstances(); i++) {
			Instance record = output.instance(i);
			String age_range = "";
			for(int dimIndex: dim) age_range += "|" + record.stringValue(dimIndex);

			if (dictionary_agerange.containsKey(age_range)) {
				ct = (Integer) dictionary_agerange.get(age_range); 
				dictionary_agerange.put(age_range, ct+1);
				dictionary_tot_income.put(age_range, income[i] + dictionary_tot_income.get(age_range));
			} else {
				dictionary_agerange.put(age_range, 1);
				dictionary_tot_income.put(age_range, income[i]);
			}
		}
		System.out.println("_____________________________________________________________________________________________________");
		for(String age_range: dictionary_agerange.keySet()) {
			System.out.printf("\n%-30s\t%f\n", age_range, dictionary_tot_income.get(age_range)/ dictionary_agerange.get(age_range));
			System.out.printf("\n%-30s\t%s\n", "COUNT(category)", dictionary_agerange.get(age_range));
		}
		System.out.println("_____________________________________________________________________________________________________");

	}


}
