
public class Start_Class {

	static boolean data_read = false;

	// Check that credentials match
	public static boolean credentials_match(String input_ID, String input_passwd) {
		return (input_ID.equals(Credential_Class.get_ID())) && 
				(input_passwd.equals(Credential_Class.get_passwd()));
	}

	// Check that sensor file exists
	public static boolean check_data(String path) {
		data_read = Sensor_Class.data_read(path);
		return data_read;
	}

	// If there is an object standing ahead of the train within 0.3 miles, then return TRUE
	public static boolean standing_obj_at_start(double distance) {
		return (distance < 0.5);
	}

	// If there is a moving object ahead, just return whether it's going above 125 mph, because that means
	// It's above our normal speed for when we start.
	public static boolean moving_obj_at_start(double speed) {
		return (speed < 125.0);
	}




}
