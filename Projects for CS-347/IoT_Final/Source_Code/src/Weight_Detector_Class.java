
public class Weight_Detector_Class {
	
	// Max cargo weight train can carry in lbs.
	private static double MAX_WEIGHT = 286000.0;
	
	public static boolean is_cargo_good(double cargo_weight) {
		return (cargo_weight < MAX_WEIGHT);
	}
	
}
