import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import weka.associations.Apriori;
import weka.associations.FPGrowth;
import weka.associations.FPGrowth.AssociationRule;
import weka.associations.FPGrowth.BinaryItem;
import weka.core.Instances;
import weka.core.SelectedTag;
import weka.core.converters.ConverterUtils.DataSource;



public class Association {
	
public static void main(String[] args) throws Exception {
	//import dataset
	String filename="supermarket.arff";
	DataSource source = new DataSource(filename);
	Instances instances = source.getDataSet();
	//delete the attribute total
	instances.deleteAttributeAt(216);
	
	FPGrowth f = new FPGrowth();
	// set the metrics to apply FP Growth 
	f.setMetricType(new SelectedTag(1,Apriori.TAGS_SELECTION));
	f.setMinMetric(1.2);
	f.setLowerBoundMinSupport(0.3);
	// This makes sure that rules show vegetables on left or right side.
	f.setRulesMustContain("vegetables");
	f.buildAssociations(instances);
	
	List<AssociationRule> listObject= new ArrayList<>();
	List<AssociationRule> finallistObject= new ArrayList<>();
	listObject=f.getAssociationRules();

	/*
	Now print out the following for each rule :
			Premise (i.e. LHS)
			Consequence (i.e. RHS)
			Total Support
			Lift
			Confidence
	 */
	// These are the rules we want to view :
	for (int i = 0; i < listObject.size(); i++) {
		if( listObject.get(i).getPremise().toString().contains("vegetables")==true)
		{
			finallistObject.add(listObject.get(i));
		}
	}
	
	System.out.println("The Final List of Rules are :");
	System.out.println();
	String format="%-40s %-40s %-15s %-10s %-10s %n";
	String numformat="%-40s %-40s %-15.2f %-10.2f %-10.2f %n";
	System.out.printf( format, "PREMISE","CONSEQUENCE","TOTAL-SUPPORT","LIFT","CONFIDENCE");
	System.out.println();
	//sort based on confidence
	if (finallistObject.size() > 0) {
	    Collections.sort(finallistObject, new Comparator<AssociationRule>() {
	        @Override	
	        public int compare(final AssociationRule object1,final AssociationRule object2) {
	            return -Double.compare(getConfidence(object1), getConfidence(object2));
	        }
	       } );
	   }
	
	for (int i = 0; i < finallistObject.size(); i++) {
		//theres is a mistake here LOL , we have printed out support twice instead of lift
		System.out.printf( numformat, finallistObject.get(i).getPremise(),finallistObject.get(i).getConsequence(),getTotalSupport(finallistObject, i),getTotalSupport(finallistObject, i),getConfidence(finallistObject.get(i)));
	}

}
public static double getTotalSupport(List<AssociationRule> obj,int i)
{
	
	return obj.get(i).getTotalSupport();
}
public static double getLift(List<AssociationRule> obj,int i)
{
	
	return obj.get(i).getMetricValue();
}
public static double getConfidence(AssociationRule obj)
{
	double conf=(double)(obj.getTotalSupport())/obj.getPremiseSupport();
	return conf;
}
}
