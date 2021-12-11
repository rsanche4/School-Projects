// Assignment 2 by Rafael Sanchez AND Tudor Tus
// I pledge my honor that I have abided by the Stevens Honor System.
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Semaphore;

public class Bakery implements Runnable {
	private static final int TOTAL_CUSTOMERS = 200;
	private static final int ALLOWED_CUSTOMERS = 50;
	private static final int FULL_BREAD = 20;
	private Map<BreadType, Integer> availableBread;
	private ExecutorService executor;
	private float sales = 0;

	// TODO
	//public Semaphore shop = new Semaphore(ALLOWED_CUSTOMERS);
	public Semaphore shelf_rye = new Semaphore(1);
	public Semaphore shelf_sour = new Semaphore(1);
	public Semaphore shelf_wond = new Semaphore(1);
	public Semaphore cashiers = new Semaphore(4);
	public Semaphore sales_mutex = new Semaphore(1);
	
	/**
	 * Remove a loaf from the available breads and restock if necessary
	 */
	public void takeBread(BreadType bread) {
		int breadLeft = availableBread.get(bread);
		if (breadLeft > 0) {
			availableBread.put(bread, breadLeft - 1);
		} else {
			System.out.println("No " + bread.toString() + " bread left! Restocking...");
			// restock by preventing access to the bread stand for some time
			try {
				Thread.sleep(1000);
			} catch (InterruptedException ie) {
				ie.printStackTrace();
			}
			availableBread.put(bread, FULL_BREAD - 1);
		}
	}

	/**
	 * Add to the total sales
	 */
	public void addSales(float value) {
		sales += value;
	}

	/**
	 * Run all customers in a fixed thread pool
	 */
	public void run() {
		availableBread = new ConcurrentHashMap<BreadType, Integer>();
		availableBread.put(BreadType.RYE, FULL_BREAD);
		availableBread.put(BreadType.SOURDOUGH, FULL_BREAD);
		availableBread.put(BreadType.WONDER, FULL_BREAD);
		// Spawn a bunch of customers and they will take care of the shopping
		// TODO
		//Bakery bakery = new Bakery();
		executor = Executors.newFixedThreadPool(ALLOWED_CUSTOMERS);
		Customer[] cust_arr = new Customer[TOTAL_CUSTOMERS];
		for (int i = 0; i < TOTAL_CUSTOMERS; i++) {
			cust_arr[i] = new Customer(this);
			executor.execute(cust_arr[i]);
		}
		executor.shutdown();
	}
}