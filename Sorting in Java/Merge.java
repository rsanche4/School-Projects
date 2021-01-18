//I pledge my Honor I have abided by the Stevens Honor System

package sortingPackage;

public class Merge {
	public static void sort(Comparable [] a) {
	//I was unsure how I would do this problem just with sort, so I decided to create multiple functions
	}

	
	
	public static void merge(Comparable[] leftArray, Comparable[] rightArray, Comparable[] a) {
		//left size is a.length/2 and right size is length of array - a.length/2
		
		int i =0;
		int j =0;
		int k= 0;
		while((j < (a.length/2)) && k<(a.length - (a.length/2))) {
			if (less(leftArray[j], rightArray[k])) {
				a[i++] = leftArray[j++];
			} else {
				a[i++] = rightArray[k++];
			}
		}
		
		while(j<a.length) {
			a[i++] = leftArray[j++];
		}
		while(k<(a.length - (a.length/2))) {
			a[i++] = rightArray[k++];
		}
	}
	
	
	

			  public static void mergeSort(Comparable [] a){
			      if (a.length == 1) {
			    	  return;
			    	  } else {
			      
			 
			      Comparable[] leftArray = new Comparable[a.length/2];
			      Comparable[] rightArray = new Comparable[a.length - (a.length/2)];
			      
			      int k = 0;
			      for (int i = 0; i < a.length; ++i)
			      {
			    	  if (i < (a.length/2)) {
			    		  leftArray[i] = a[i];
			    	  } else {
			    		  rightArray[k] = a[i];
			    		  k++;
			    	  }
			      }
			      
			      mergeSort(leftArray);
			      mergeSort(rightArray);
			      merge(leftArray, rightArray, a);
			      
			  }
			  }
	
			  private static boolean less(Comparable a, Comparable b) {
					return a.compareTo(b) < 0;
				}
	
}
