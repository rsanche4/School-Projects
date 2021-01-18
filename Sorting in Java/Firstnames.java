//Rafael Sanchez
//I pledge my Honor I have abided by the Stevens Honor System

package sortingPackage;

public class Firstnames implements Comparable<Firstnames> {
	private final String name;
	
	public Firstnames(String n) {
		name = n;
	}
	public int compareTo(Firstnames that) {
		if (this.name.charAt(0) > that.name.charAt(0))
			return 1;
		if (this.name.charAt(0) < that.name.charAt(0))
			return -1;
		else {
			return 0;
		}
	}
	
	public String toString() {
		return "" + name; 
	}
}
