//Rafael Sanchez
//I pledge my Honor I have abided by the Stevens Honor System

package sortingPackage;

public class Bubble {
	public static void sort(Comparable [] a) {
		int N = a.length;
		for (int i = 0; i < N-1; i++) {
			for (int j = 0; j< N-i-1; j++) {
				if (less(a[j], a[j+1]) == false) {
					Comparable temporary;
					temporary = a[j];
					a[j] = a[j+1];
					a[j+1] = temporary;
				}
			}
		}
	}
	private static boolean less(Comparable a, Comparable b) {
		return a.compareTo(b) < 0;
	}
}
