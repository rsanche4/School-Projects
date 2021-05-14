import java.io.File;

public class Sensor_Class {

	public static double standing_objdist;
	public static double movobj_speed_ahead;
	public static double movobj_speed_behind;
	public static int rpm;

	// Checks that a file is given and we can read from it
	public static boolean data_read(String path) {
		
		File INPUT = new File(path);
		return (INPUT.exists());
	}

	// Convert rpm to miles per hour
	public static double rpmToMph(int rotationsPerMin) {
		double circumference = 0.003;
		return (circumference * rotationsPerMin * 60);
	}


}
