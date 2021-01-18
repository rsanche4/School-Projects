//Rafael Sanchez
//I pledge my Honor I have abided by the Stevens Honor System

package sortingPackage;

public class Selection {
	
	
	public static void sort(Comparable [] a) {
		int n = a.length; 
		for (int j = 0; j < n; j++) {
			int iMin = j;
			for (int i = j + 1; i<n; i++) {
				if (less(a[i], a[iMin])) {
					iMin = i;
					
				}
					if (iMin != j) {
						Comparable temp;
						temp = a[iMin];
						a[iMin] = a[j];
						a[j] = temp;
					
					}
			}
		}
	}
	private static boolean less(Comparable a, Comparable b) {
		return a.compareTo(b) < 0;
	}
	
	
}
