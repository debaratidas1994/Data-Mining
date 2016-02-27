
import java.util.Random;

import weka.classifiers.Classifier;
import weka.classifiers.trees.BFTree;
import weka.classifiers.trees.J48;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;


public class DecisionTree {

	
	public static void main(String[] args) throws Exception{
		
		String filename="bank-data2.arff";
		DataSource source = new DataSource(filename);
		Instances instances = source.getDataSet();
		// randomise the instances
		instances.setClassIndex(instances.numAttributes()-1);
		Random rand=new Random();
		Instances ran_data=new Instances(instances);
		ran_data.randomize(rand);
		// train the dataset based on folds , here number of instances is 600
		// therefore 600/60 = 10, 590 
		Instances trainingSet=ran_data.trainCV(60, 0);
		trainingSet.setClassIndex(instances.numAttributes()-1);
		
		
		Instances testSet=ran_data.testCV(60, 1);
		testSet.setClassIndex(instances.numAttributes()-1);
		// classify based on J48
		Classifier model = new J48();
		model.buildClassifier(trainingSet);
		System.out.println(model);
		// classify based on BFTree
		Classifier model1 = new BFTree();
		model1.buildClassifier(trainingSet);
		System.out.println();
		System.out.println(model1);
		// Print out result
		String format="\n%-30s%-30s%-30s";
		System.out.printf(format,"Class","Class predicted by C4.5","Class Predicted by Gini");
		System.out.println();
		for (int i = 0; i < testSet.numInstances(); i++) {
			Instance test = testSet.instance(i);
			int m=(int)model.classifyInstance(test);
			int m1=(int)model1.classifyInstance(test);
			System.out.printf(format,
					test.stringValue(instances.numAttributes()-1), 
				test.classAttribute().value(m),
				test.classAttribute().value(m1)
				);
			
		}
		System.out.println();
		
}
	
}
