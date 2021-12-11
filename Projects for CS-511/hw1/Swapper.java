public class Swapper implements Runnable {
    private int offset;
    private Interval interval;
    private String content;
    private char[] buffer;

    public Swapper(Interval interval, String content, char[] buffer, int offset) {
        this.offset = offset;
        this.interval = interval;
        this.content = content;
        this.buffer = buffer;
    }

    @Override
    public void run() {
        // TODO: Implement me!
    	int start_ind = interval.getX();
    	int end_ind = interval.getY();
    	int k = 0;
    	for (int i = start_ind; i <= end_ind; i++) {
    			buffer[offset+k] = content.charAt(i);
    			k++;
    	}
    }
}