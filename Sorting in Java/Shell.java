//Rafael Sanchez
//I pledge my Honor I have abided by the Stevens Honor System

package sortingPackage;

public class Shell {
	public static void sort(Comparable [] arr) {
		int N = arr.length;
		for (int gap = N / 2; gap > 0; gap = gap /2) {
	        for (int i = gap; i < N; i++) {
	            Comparable k = arr[i];
	            int j = i;
	            while (j >= gap && (less(arr[j - gap], k) == false)) {
	                arr[j] = arr[j - gap];
	                j -= gap;
	            }
	            arr[j] = k;
	        }
	    }
	}
	
	private static boolean less(Comparable a, Comparable b) {
		return a.compareTo(b) < 0;
	}
	
}
