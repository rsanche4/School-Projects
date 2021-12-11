import java.io.*;
import java.util.*;

public class TextSwap {

	private static String readFile(String filename, int chunkSize) throws Exception {
		String line;
		StringBuilder buffer = new StringBuilder();
		File file = new File(filename);
		// The "-1" below is because of this:
		// https://stackoverflow.com/questions/729692/why-should-text-files-end-with-a-newline
		// #TODO I need to put this back to normal 
		//if ((file.length()-1) % chunkSize!=0)
		if (file.length() % chunkSize!=0)
		{ throw new Exception("File size not multiple of chunk size"); };
		BufferedReader br = new BufferedReader(new FileReader(file));
		while ((line = br.readLine()) != null){
			buffer.append(line);
		}
		br.close();
		return buffer.toString();
	}

	private static Interval[] getIntervals(int numChunks, int chunkSize) {
		// TODO: Implement me!
		// Get the number of chunks and label them according to their letter in the alphabet
		char[] ALPHA = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};
		// Note: number of chunks contain the place where we should stop reading from the alphabet
		//int[][] intervals_array = new int[numChunks][2];
		Interval[] intervals_array = new Interval[numChunks];
		// So now get the intervals from each chunk
		StringBuilder letters_str = new StringBuilder("");
		for (int i = 0; i < numChunks; i++) {
			for (int k = 0; k < chunkSize; k++) {
				letters_str.append(ALPHA[i]);
			}
		}
		// So now go through the whole string and write the index of each letter
		int start_index = 0;
		int end_index = 0;
		int intervals_index = 0;

		for (int p = 0; p < letters_str.length(); p++) {
			if (p == 0) {
				start_index = p;
			} else if (p == letters_str.length()-1) {
				end_index = p;
				Interval temp = new Interval(start_index,end_index);
				intervals_array[intervals_index] = temp;
				break;
			} else if (letters_str.charAt(p) != letters_str.charAt(p+1)) {
				end_index = p;
				// Insert in intervals array
				Interval temp = new Interval(start_index,end_index);
				intervals_array[intervals_index] = temp;
				
				intervals_index++;
				
				start_index = p+1;
				
			}
		}
		
		return intervals_array; // return array of intervals
	}

	private static List<Character> getLabels(int numChunks) {
		Scanner scanner = new Scanner(System.in);
		List<Character> labels = new ArrayList<Character>();
		int endChar = numChunks == 0 ? 'a' : 'a' + numChunks - 1;
		System.out.printf("Input %d character(s) (\'%c\' - \'%c\') for the pattern.\n", numChunks, 'a', endChar);
		for (int i = 0; i < numChunks; i++) {
			labels.add(scanner.next().charAt(0));
		}
		scanner.close();
		// System.out.println(labels);
		return labels;
	}

	private static char[] runSwapper(String content, int chunkSize, int numChunks) {
		List<Character> labels = getLabels(numChunks);
		Interval[] intervals = getIntervals(numChunks, chunkSize);
		// TODO: Order the intervals properly, then run the Swapper instances.
		// So my question: What is runSwapper returning? Is it returning what is going to be wriiten to the output.txt?
		// If so, I can just do it without running threads, right? Or is it working together with the Swapper.java class?
		// What's the Swapper.java class doing exactly? Is it creating a bunch of threads in the run method? Is each thread taking the intervals to be changed?
		// MAJOR QUESTION: WHERE ARE THE THREADS BEING CREATED AND RUN?
		
		
		// Second understanding: We are not using threads, but rather Swapper acts as a thread? If that's the case,
		// Then what does Swapper Run() method do? So I get it will do the swapping, but my question is what is char[] buffer? is it the whole resulting swapped string?
		char[] alpha = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
		char[] ALPHA = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};
		char[] buf = new char[content.length()];
		for (int i = 0; i < numChunks; i++) {
			int temp = 0;
			if (labels.contains(alpha[i])) {
				temp = labels.indexOf(alpha[i]);
			} else if (labels.contains(ALPHA[i])) {
				temp = labels.indexOf(ALPHA[i]);
			}
			int offset = intervals[temp].getX();
			new Thread(new Swapper(intervals[i], content, buf, offset)).start();
		}
		return buf;
	}

	private static void writeToFile(String contents, int chunkSize, int numChunks) throws Exception {
		char[] buff = runSwapper(contents, chunkSize, contents.length() / chunkSize);
		PrintWriter writer = new PrintWriter("output.txt", "UTF-8");
		writer.print(buff);
		writer.close();
	}

	public static void main(String[] args) {
		if (args.length != 2) {
			System.out.println("Usage: java TextSwap <chunk size> <filename>");
			return;
		}
		String contents = "";
		int chunkSize = Integer.parseInt(args[0]);
		try {
			contents = readFile(args[1],chunkSize);
			writeToFile(contents, chunkSize, contents.length() / chunkSize);
		} catch (Exception e) {
			System.out.println("Error with IO.");
			return;
		}
	}
}
