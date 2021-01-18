package sortingPackage;

public class Quick {
	//hi is a.length-1   and low is 0
	public static void sort(Comparable[] a) {
		quickSort(a, 0, a.length-1);
	}
	
	public static void quickSort(Comparable[] a, int low, int high) {
		if (low < high)
		{
			int pi = partition(a, low, high);
			quickSort(a, low, pi-1);
			quickSort(a, pi+1, high);
		}
	}
	public static int partition(Comparable[] a, int low, int high) {
		Comparable pivot = a[high];
		int i = low-1;
		for (int j = low; j<high; j++) {
			if (less(a[j], pivot)) {
				i++;
				
				Comparable temp = a[i];
				a[i] = a[j];
				a[j] = temp;
			}
		}
		
		Comparable temp = a[i+1];
		a[i+1] = a[high];
		a[high] = temp;
		
		return i+1;
	}
	
	private static boolean less(Comparable a, Comparable b) {
		return a.compareTo(b) < 0;
	}
}
