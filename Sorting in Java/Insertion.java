//Rafael Sanchez
//I pledge my Honor I have abided by the Stevens Honor System

package sortingPackage;

public class Insertion {
	public static void sort(Comparable [] a) {
		for (int i = 0; i < a.length; i++) {
			for (int j = i; j > 0; j--) {
				if (less(a[j], a[j-1])) {
				Comparable temporary;
				temporary = a[i];
				a[i] = a[j];
				a[j] = temporary;
				} else {
					break;
				}
				}
			
			}
		}
	private static boolean less(Comparable a, Comparable b) {
		return a.compareTo(b) < 0;
	}
	
	}
