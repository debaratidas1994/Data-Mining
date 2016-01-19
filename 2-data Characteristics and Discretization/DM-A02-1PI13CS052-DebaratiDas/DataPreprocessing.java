package asgn2;


import weka.core.Instances;
import weka.core.Attribute;
import weka.core.converters.ConverterUtils.DataSource;
import weka.core.AttributeStats;
import weka.experiment.Stats;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Discretize;

// Data Mining - Data Characteristics and Discretization Example

public class DataPreprocessing {
		
	public static void main (String args[]) {
		String filename = "bank-data.csv";
		DataSource source;
		try {
			// Create new data source
			source = new DataSource(filename);
			// Read instances from the CSV file
			
			Instances instances = source.getDataSet();
			
			// Delete the ID attribute
			instances.deleteAttributeAt(0);
			
			 //Print header and instances of the dataset 
			 //System.out.println("\nDataset:\n");
			 //System.out.println(instances);
			 
			// Get the statistics for attribute at index 0 (now age)
			int index = 0;
			double var, sdev1,sdev2,sdevf,sdevm;
			double mean1, mean2;
			Attribute attr = instances.attribute(index);
			var=instances.variance(0);
			sdev1=Math.sqrt(var);  //use in covar and correlation
			sdevf=(double)Math.round(sdev1 * 1000d) / 1000d;
			AttributeStats astats = instances.attributeStats(index);
			Stats stats = astats.numericStats;
			
			mean1=stats.mean;  //use in covar and correlation
			
			System.out.println("The Statistical Contents are :");
			String format = "%-10s%-10s%-10s%-60s";
			System.out.printf(format, "Min", "Max", "Mean","Std-Dev");
			System.out.println();
			System.out.printf(format, String.valueOf(stats.min),String.valueOf(stats.max),String.valueOf(stats.mean),String.valueOf(sdevf));
			System.out.println();
			// Get the statistics for attribute at index 3 (now income)
			index = 3;
			attr = instances.attribute(index);
			var=instances.variance(3);
			sdev2=Math.sqrt(var);  //use in covar and correlation
			
			sdevf=(double)Math.round(sdev2 * 1000d) / 1000d;
			
			astats = instances.attributeStats(index);
			stats = astats.numericStats;
			
			mean2=stats.mean; //use in covar and correlation
			
			sdevm=(double)Math.round(mean2 * 1000d) / 1000d;

			System.out.printf(format, String.valueOf(stats.min),String.valueOf(stats.max),String.valueOf(sdevm),String.valueOf(sdevf));
			System.out.println();
			
			
			//get the values of attribute at index 0 and 3 into some double array so that covariance and correlation can be done
			//get number of instances
			
			int numInst = instances.numInstances();
			double [] result = new double[numInst]; // stores age instance
			double [] result1 = new double[numInst]; // stores income instance
			
			for (int i = 0; i < result.length; i++) 
			{
				result[i] = instances.instance(i).value(0);
				result1[i] = instances.instance(i).value(3);
			}
			
			// Calculate covariance between Age and Income
			
			double covar=GetCovariance(result,result1,mean1,mean2,numInst);
			System.out.println("Covariance between age and income is :"+String.valueOf(covar));
			
			// Calculate correlation between Age and Income
			
			double corel=GetCorrelation(covar,sdev1,sdev2);
			System.out.println("Correlation between age and income is :"+String.valueOf(corel));
			
			
	
			
			// Using unsupervised Discretize (see import)
			Discretize filter = new Discretize();
			filter.setAttributeIndices("4");
			// Set number of bins
			filter.setBins(4);
			filter.setInputFormat(instances);
			Instances output = Filter.useFilter(instances, filter);
			Attribute atrrincome=output.attribute(3);
			AttributeStats astatsincome=output.attributeStats(3);
			double[] cutPoints = filter.getCutPoints(3);
			//print out the cutpoints and the frequencies in each bin
			System.out.println("Cut points are :");
			for(int i =0;i<cutPoints.length;i++)
			{
				System.out.println(cutPoints[i]);
			}
	        //print out frequency and cut points in each bin 
			int[] freq=astatsincome.nominalCounts;
			System.out.println("Frequencies in four bins are :");
			for(int i =0;i<freq.length;i++)
			{
				System.out.println(freq[i]);
			}
			
			//to be done
			
		} catch (Exception e) { e.printStackTrace();
		}
	}

static double GetCovariance(double[] result,double[] result1,double mean1,double mean2,int numInst)
{
	double sums=0.0;
	for(int i=0;i<numInst;i++)
	{
		sums+=result[i]*result1[i];
	}
	return (sums/numInst)-(mean1*mean2);
}
static double GetCorrelation(double covar,double sdev1,double sdev2)
{
	return((covar)/(sdev1*sdev2));
}
} 
