//Rafael Sanchez
//I pledge my Honor I have abided by the Stevens Honor System

package sortingPackage;

import java.util.Arrays;

public class MyTest {
	
	private static long average(long[] array)
	{
		long sum = 0;
		for (int i=0; i < array.length; i++) {
			sum += array[i];
		}
		return sum / array.length;
	}
	
	
	
	public static void main(String args[]) {
		
		//array of Firstnames was generated
		System.out.println("Test for Firstnames");
		Firstnames raf = new Firstnames("Rafael");
		Firstnames leo = new Firstnames("Leo");
		Firstnames bry = new Firstnames("Bryant");
		Firstnames nid = new Firstnames("Nidhi");
		Firstnames pat = new Firstnames("Patrick");
		Comparable[] namesArray = new Comparable[5];
		namesArray[0] = raf;
		namesArray[1] = leo;
		namesArray[2] = bry;
		namesArray[3] = nid;
		namesArray[4] = pat;		
		
		System.out.println(Arrays.toString(namesArray));
		
		//Below I am testing 100 times for each algorithms for Firstnames
		
		//this is the array that's going to be storing all 100 times elapsed
		long[] arrayTimes = new long[100];
		
		//Selection
		for (int i = 0; i < arrayTimes.length; i++) {
		long startTime = System.nanoTime();
		
		Selection.sort(namesArray);
		
		long endTime = System.nanoTime();
		long timeElapsed = endTime - startTime;
		arrayTimes[i] = timeElapsed;
		}
		System.out.println("Time average for Selection: " + average(arrayTimes));
		System.out.println(Arrays.toString(namesArray));
		
		
		
		//Insertion
		for (int i = 0; i < arrayTimes.length; i++) {
		long startTime = System.nanoTime();
		
		Insertion.sort(namesArray);
				
		long endTime = System.nanoTime();
		long timeElapsed = endTime - startTime;
		arrayTimes[i] = timeElapsed;
		}
		System.out.println("Time average for Insertion: " + average(arrayTimes));
		System.out.println(Arrays.toString(namesArray));
		
		
		//Bubble
		for (int i = 0; i < arrayTimes.length; i++) {
		long startTime = System.nanoTime();
			
		Bubble.sort(namesArray);
					
		long endTime = System.nanoTime();
		long timeElapsed = endTime - startTime;
		arrayTimes[i] = timeElapsed;
		}
		System.out.println("Time average for Bubble: " + average(arrayTimes));
		System.out.println(Arrays.toString(namesArray));
		
		//Shell
		for (int i = 0; i < arrayTimes.length; i++) {
		long startTime = System.nanoTime();
			
		Shell.sort(namesArray);
					
		long endTime = System.nanoTime();
		long timeElapsed = endTime - startTime;
		arrayTimes[i] = timeElapsed;
		}
		System.out.println("Time average for Shell: " + average(arrayTimes));
		System.out.println(Arrays.toString(namesArray));
		
		//Merge
		for (int i = 0; i < arrayTimes.length; i++) {
		long startTime = System.nanoTime();
				
		Merge.sort(namesArray);
					
		long endTime = System.nanoTime();
		long timeElapsed = endTime - startTime;
		arrayTimes[i] = timeElapsed;
		}
		System.out.println("Time average for Merge: " + average(arrayTimes));
		System.out.println(Arrays.toString(namesArray));
		
		//Quick
		for (int i = 0; i < arrayTimes.length; i++) {
		long startTime = System.nanoTime();
					
		Quick.sort(namesArray);
						
		long endTime = System.nanoTime();
		long timeElapsed = endTime - startTime;
		arrayTimes[i] = timeElapsed;
		}
		System.out.println("Time average for Quick: " + average(arrayTimes));
		System.out.println(Arrays.toString(namesArray));
		
		
		
		
		
		
		
		
		////array of Dates was generated
		
		
		System.out.println("Tests for Dates");
		//testing birthdays below
		Date rafBirth = new Date(8, 12, 2000);
		Date catBirth = new Date(8, 9, 2000);
		Date friBirth = new Date(4, 8, 2005);
		Date leoBirth = new Date(1, 1, 1998);
		Date gamBirth = new Date(7, 6, 1987);
		Comparable[] birthArray = new Comparable[5];
		birthArray[0] = rafBirth;
		birthArray[1] = catBirth;
		birthArray[2] = friBirth;
		birthArray[3] = leoBirth;
		birthArray[4] = gamBirth;
		
		
		System.out.println(Arrays.toString(birthArray));
		
		//down below we are getting the averages
				//Selection
				for (int i = 0; i < arrayTimes.length; i++) {
				long startTime = System.nanoTime();
				
				Selection.sort(birthArray);
				
				long endTime = System.nanoTime();
				long timeElapsed = endTime - startTime;
				arrayTimes[i] = timeElapsed;
				}
				System.out.println("Time average for Selection: " + average(arrayTimes));
				System.out.println(Arrays.toString(birthArray));
				
				
				
				//Insertion
				for (int i = 0; i < arrayTimes.length; i++) {
				long startTime = System.nanoTime();
				
				Insertion.sort(birthArray);
						
				long endTime = System.nanoTime();
				long timeElapsed = endTime - startTime;
				arrayTimes[i] = timeElapsed;
				}
				System.out.println("Time average for Insertion: " + average(arrayTimes));
				System.out.println(Arrays.toString(birthArray));
				
				
				//Bubble
				for (int i = 0; i < arrayTimes.length; i++) {
				long startTime = System.nanoTime();
					
				Bubble.sort(birthArray);
							
				long endTime = System.nanoTime();
				long timeElapsed = endTime - startTime;
				arrayTimes[i] = timeElapsed;
				}
				System.out.println("Time average for Bubble: " + average(arrayTimes));
				System.out.println(Arrays.toString(birthArray));
				
				//Shell
				for (int i = 0; i < arrayTimes.length; i++) {
				long startTime = System.nanoTime();
					
				Shell.sort(birthArray);
							
				long endTime = System.nanoTime();
				long timeElapsed = endTime - startTime;
				arrayTimes[i] = timeElapsed;
				}
				System.out.println("Time average for Shell: " + average(arrayTimes));
				System.out.println(Arrays.toString(birthArray));
				
				//Merge
				for (int i = 0; i < arrayTimes.length; i++) {
				long startTime = System.nanoTime();
						
				Merge.sort(birthArray);
							
				long endTime = System.nanoTime();
				long timeElapsed = endTime - startTime;
				arrayTimes[i] = timeElapsed;
				}
				System.out.println("Time average for Merge: " + average(arrayTimes));
				System.out.println(Arrays.toString(birthArray));
				
				//Quick
				for (int i = 0; i < arrayTimes.length; i++) {
				long startTime = System.nanoTime();
							
				Quick.sort(birthArray);
								
				long endTime = System.nanoTime();
				long timeElapsed = endTime - startTime;
				arrayTimes[i] = timeElapsed;
				}
				System.out.println("Time average for Quick: " + average(arrayTimes));
				System.out.println(Arrays.toString(birthArray));
		
		
	}
}
