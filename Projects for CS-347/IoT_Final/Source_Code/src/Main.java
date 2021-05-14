import java.awt.Color;
import javax.swing.*;
import java.util.Scanner;
import java.io.*;
import java.awt.event.*;
import javax.sound.sampled.*;


public class Main implements ActionListener {
	
	// Here we have the path of error image. Change accordingly to run on a different system.
	private static String warning_icon = "C:\\Users\\rafas\\eclipse-workspace\\HTR\\error.png";
	private static String check_icon = "C:\\Users\\rafas\\eclipse-workspace\\HTR\\green_check.png";
	private static String standing_icon = "C:\\Users\\rafas\\eclipse-workspace\\HTR\\standing_obj.png";
	private static String movobjFront_icon = "C:\\Users\\rafas\\eclipse-workspace\\HTR\\objFront.png";
	private static String movobjBack_icon = "C:\\Users\\rafas\\eclipse-workspace\\HTR\\objBack.png";
	private static String rail_icon = "C:\\Users\\rafas\\eclipse-workspace\\HTR\\rail_ahead.png";
	private static String rail_open_icon = "C:\\Users\\rafas\\eclipse-workspace\\HTR\\rail.png";
	private static String sec5_icon = "C:\\Users\\rafas\\eclipse-workspace\\HTR\\5sec.png";
	private static String wheels_icon = "C:\\Users\\rafas\\eclipse-workspace\\HTR\\wheels.png";
	private static String music_path = "C:\\Users\\rafas\\eclipse-workspace\\HTR\\IoTTheme.wav";
	private static String data_path;
	private static JPanel panel;
	private static JLabel userLabel; 
	private static JTextField userText;
	private static JLabel pwdLabel;
	private static JPasswordField pwdText;
	private static JLabel error_on_login;
	private static JFrame frame;
	private static JButton loginbutton;
	private static JButton button1;
	private static JButton buttonLoop;
	private static Scanner reader;
	private static int timeElapsed = 0;
	
	public static void main_body_loop() {
		
		 //Enter the main body
		if (reader.hasNext()) {
			panel.removeAll();
			
			
			boolean no_problems = true;

			Sensor_Class.standing_objdist = Double.parseDouble(reader.next());
			Sensor_Class.movobj_speed_ahead = Double.parseDouble(reader.next());
			Sensor_Class.movobj_speed_behind = Double.parseDouble(reader.next());
			GPS_Data_Class.railroad_dist = Double.parseDouble(reader.next());
			GPS_Data_Class.railroad_func_status = Integer.parseInt(reader.next());
			GPS_Data_Class.train_speed = Double.parseDouble(reader.next());
			Sensor_Class.rpm = Integer.parseInt(reader.next());
			
			timeElapsed++;
			String time = "Time elapsed: " + String.valueOf(timeElapsed);
			JLabel timeLabel = new JLabel(time);
			timeLabel.setBounds(1280/2 - 60 - 10, 30,450,100);
			panel.add(timeLabel);
			
			// Next we are going to check each of them
			if (Sensor_Class.standing_objdist < 1.0) {
				JLabel standing_objLabel = new JLabel("Warning: There is a standing object ahead of the train.");
				standing_objLabel.setBounds(20+10, 120, 500, 25);
				panel.add(standing_objLabel);
				
				JLabel labelStand=new JLabel();
				labelStand.setIcon(new ImageIcon(standing_icon));
				labelStand.setBounds(20+10+20+35, 120, 200, 200);
				panel.add(labelStand);
				
				no_problems = false;
			}

			if (Sensor_Class.movobj_speed_ahead < GPS_Data_Class.train_speed) {
				JLabel moving_objFront = new JLabel("Warning: There is a moving object ahead of the train.");
				moving_objFront.setBounds(1280/2 - 200 +10, 120, 500, 25);
				panel.add(moving_objFront);
				
				JLabel labelMov=new JLabel();
				labelMov.setIcon(new ImageIcon(movobjFront_icon));
				labelMov.setBounds(1280/2 - 200 +10 + 20+10+20+35, 125, 200, 200);
				panel.add(labelMov);
				
				no_problems = false;
			}

			if (Sensor_Class.movobj_speed_behind > GPS_Data_Class.train_speed) {
				JLabel moving_objBehind = new JLabel("Warning: There is a moving object behind the train.");
				moving_objBehind.setBounds(1280/2 + 200 + 10, 120, 500, 25);
				panel.add(moving_objBehind);
				
				JLabel labelMov2=new JLabel();
				labelMov2.setIcon(new ImageIcon(movobjBack_icon));
				labelMov2.setBounds(1280/2 + 200 + 10 + 20+10+20+35, 125, 200, 200);
				panel.add(labelMov2);
				
				no_problems = false;
			}

			if (GPS_Data_Class.railroad_dist < 1.0 && GPS_Data_Class.railroad_dist > 0.0) {
				JLabel railroad_obj = new JLabel("Warning: There is a railroad crossing ahead. Honk horn for:");
				railroad_obj.setBounds(20+10, 120 + 200, 500, 25);
				panel.add(railroad_obj);
				
				JLabel labelRail=new JLabel();
				labelRail.setIcon(new ImageIcon(rail_icon));
				labelRail.setBounds(10+20+35+20, 120 + 200 + 30, 200, 200);
				panel.add(labelRail);
				
				no_problems = false;
			}
			
			if (GPS_Data_Class.railroad_dist <= 0.0) {
				JLabel honk = new JLabel("Warning: You arrived at a railroad crossing. Honk horn for:");
				honk.setBounds(20+10, 120 + 200, 500, 25);
				panel.add(honk);
				
				JLabel label5=new JLabel();
				label5.setIcon(new ImageIcon(sec5_icon));
				label5.setBounds(10+20+35+20, 120 + 200 + 30, 200, 200);
				panel.add(label5);
				
				no_problems = false;
			}

			if (GPS_Data_Class.railroad_func_status == 0) {
				JLabel rail_not_working = new JLabel("Warning: The railroad crossing ahead is not closing.");
				rail_not_working.setBounds(1280/2 - 200 +10, 120 + 200, 500, 25);
				panel.add(rail_not_working);
				
				JLabel labelRailOpen=new JLabel();
				labelRailOpen.setIcon(new ImageIcon(rail_open_icon));
				labelRailOpen.setBounds(1280/2 - 200 +10+ 10+20+35, 120 + 200 + 30, 200, 200);
				panel.add(labelRailOpen);
				
				no_problems = false;
			}


			if (Math.abs(GPS_Data_Class.train_speed - Sensor_Class.rpmToMph(Sensor_Class.rpm)) > 0.1) {
				JLabel wheel_slip = new JLabel("Warning: Wheels are slipping.");
				wheel_slip.setBounds(1280/2 + 200 + 10, 120 + 200, 500, 25);
				panel.add(wheel_slip);
				
				JLabel labelWheel=new JLabel();
				labelWheel.setIcon(new ImageIcon(wheels_icon));
				labelWheel.setBounds(1280/2 + 200 + 10+ 10+20+35, 120 + 200 + 30, 200, 200);
				panel.add(labelWheel);
				
				no_problems = false;
			}

			if (no_problems) {
				JLabel labelcheck=new JLabel();
				labelcheck.setIcon(new ImageIcon(check_icon));
				labelcheck.setBounds(1280/2 - 200 -20, 150,450,400);
				panel.add(labelcheck);
				no_problems = false;
			}
			
			buttonLoop = new JButton("Continue");
			buttonLoop.setBounds(1280/2 - 110, 600, 150, 25);
			buttonLoop.addActionListener(new Main());
			panel.add(buttonLoop);
			
			frame.repaint();
			// Simulate the Time Sensitive Networking Router
			//TimeUnit.SECONDS.sleep(10);
		} else {
			panel.removeAll();
			JLabel thank_you = new JLabel("IoT finished reading data. Thank you for choosing HTR IoT!");
			thank_you.setBounds(1280/2 - 150 -65, 200, 80*2*2*2, 25*2);
			panel.add(thank_you);
			frame.repaint();
		}
		
	}
	
	public static void check_at_start() {
		if (!Start_Class.check_data(data_path)) {
			JLabel error_reading = new JLabel("Error: Data from sensors and/or GPS could not be read correctly.");
			error_reading.setBounds(1280/2 - 150 -65, 200, 80*2*2*2, 25*2);
			panel.add(error_reading);
			
			
			JLabel label5=new JLabel();
			label5.setIcon(new ImageIcon(warning_icon));
			label5.setBounds(1280/2 - 90, 250,450,100);
			panel.add(label5);
			
			frame.repaint();
		} else {
			
				boolean no_warnings = true;
				// And now check for the distance of the standing object at start
				Sensor_Class.standing_objdist = Double.parseDouble(reader.next());
				if (Start_Class.standing_obj_at_start(Sensor_Class.standing_objdist)) {
					JLabel standing_start = new JLabel("Warning at start: There is a standing object ahead of the train.");
					standing_start.setBounds(1280/2 - 160, 180, 500, 25);
					panel.add(standing_start);
					no_warnings = false;
				}

				Sensor_Class.movobj_speed_ahead = Double.parseDouble(reader.next());
				if (Start_Class.moving_obj_at_start(Sensor_Class.movobj_speed_ahead)) {
					JLabel moving_start = new JLabel("Warning at start: There is a moving object ahead of the train.");
					moving_start.setBounds(1280/2 - 160, 250, 500, 25);
					panel.add(moving_start);
					no_warnings = false;
				}

				double current_cargo = Double.parseDouble(reader.next());
				if (!Weight_Detector_Class.is_cargo_good(current_cargo)) {
					JLabel cargo_start = new JLabel("Warning at start: There is too much cargo on the train.");
					cargo_start.setBounds(1280/2 - 160, 320, 500, 25);
					panel.add(cargo_start);
					no_warnings = false;
				}
				
				if (no_warnings) {
					JLabel good = new JLabel("No problems starting IoT.");
					good.setBounds(1280/2 - 100, 200, 80*2, 25*2);
					panel.add(good);
				} else {
					JLabel labelEr=new JLabel();
					labelEr.setIcon(new ImageIcon(warning_icon));
					labelEr.setBounds(1280/2 - 60, 50,450,100);
					panel.add(labelEr);
				}
				
				button1 = new JButton("Continue");
				button1.setBounds(1280/2 - 100, 400, 80*2, 25*2);
				button1.addActionListener(new Main());
				panel.add(button1);
				
				frame.repaint();
							
		}
	}
	
	// The program will run through here
	public static void main(String args[]) {

		if (args.length != 1) {
			System.out.println("Usage: java Main.java <FILE PATH>");
			return;
		}
		data_path = args[0];
		Sensor_Class.data_read(data_path);
		
		File file = new File(music_path);
		try {
			AudioInputStream audioStream = AudioSystem.getAudioInputStream(file);
			Clip clip = AudioSystem.getClip();
			clip.open(audioStream);
			clip.start();
		} catch (Exception t) {
			System.out.println("Exception: Couldn't play audio.");
		}
		
		// Set up the GUI
		panel = new JPanel();
		frame = new JFrame();
		frame.setSize(1280, 720);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setTitle("HTR IoT!");
		frame.add(panel);
		frame.setVisible(true);
		
		panel.setLayout(null);
		panel.setBackground(new Color(230, 255, 255));
		
		userLabel = new JLabel("User");
		userLabel.setBounds(1280/2 - 150 -100, 200, 80*2, 25*2);
		panel.add(userLabel);
		
		userText = new JTextField();
		userText.setBounds(1280/2 - 50 -100, 200, 165*2, 25*2);
		panel.add(userText);
		
		pwdLabel = new JLabel("Password");
		pwdLabel.setBounds(1280/2 - 150 -100, 300, 80*2, 25*2);
		panel.add(pwdLabel);
		
		pwdText = new JPasswordField();
		pwdText.setBounds(1280/2 - 50 -100, 300, 165*2, 25*2);
		panel.add(pwdText);
		
		error_on_login = new JLabel("");
		error_on_login.setBounds(1280/2 - 150 -100, 500, 165*2, 25*2);
		panel.add(error_on_login);
		
		loginbutton = new JButton("Login");
		loginbutton.setBounds(1280/2 - 150 -100, 400, 165*2 + 100, 25*2);
		loginbutton.addActionListener(new Main());
		panel.add(loginbutton);
		
		frame.repaint();
	}
	
	// This code runs if you click the button
	@Override
	public void actionPerformed(ActionEvent e) {
		if (e.getSource() == loginbutton) {
			String user = userText.getText();
			String password = pwdText.getText();
			try {
				reader = new Scanner(new File(data_path));
			} catch (Exception E) {
				System.out.println("Exception");
			}
			if (Start_Class.credentials_match(user, password)) {
				panel.removeAll();
				check_at_start();
			} else {
				error_on_login.setText("Error: Invalid User Id or Password");
			}
		} else if (e.getSource() == button1) {
			main_body_loop();
		} else if (e.getSource() == buttonLoop) {
			main_body_loop();
		}
		
	}
}		