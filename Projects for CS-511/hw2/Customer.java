// Assignment 2 by Rafael Sanchez AND Tudor Tus
// I pledge my honor that I have abided by the Stevens Honor System.
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class Customer implements Runnable {
	private Bakery bakery;
	private Random rnd = new Random();
	private List<BreadType> shoppingCart;
	private int shopTime;
	private int checkoutTime;

	/**
	 * Initialize a customer object and randomize its shopping cart
	 */
	public Customer(Bakery bakery) {
		// TODO 
		this.bakery = bakery;
		
		shopTime = rnd.nextInt(1000); 

		checkoutTime = rnd.nextInt(1000);
		shoppingCart = new ArrayList<BreadType>();
		fillShoppingCart(); 

	}

	/**
	 * Run tasks for the customer
	 */
	public void run() {
		// TODO

		
		for (int i = 0; i < shoppingCart.size(); i++) {
			if (shoppingCart.get(i) == BreadType.RYE) {
				try {
					bakery.shelf_rye.acquire();
					System.out.println("Customer " + hashCode() + " is shopping for " + shopTime + " miliseconds, at rye shelf.");
					bakery.takeBread(shoppingCart.get(i));
					Thread.sleep(shopTime);
					System.out.println("Customer " + hashCode() + " finished at rye shelf.");
					bakery.shelf_rye.release();
					continue;
				} catch (Exception e) {
					System.out.println("Error: Customer malfunctioned.");
				}

			}
			if (shoppingCart.get(i) == BreadType.SOURDOUGH) {
				try {
					bakery.shelf_sour.acquire();
					System.out.println("Customer " + hashCode() + " is shopping for " + shopTime + " miliseconds, at sourdough shelf.");
					bakery.takeBread(shoppingCart.get(i));
					Thread.sleep(shopTime);
					System.out.println("Customer " + hashCode() + " finished at sourdough shelf.");
					bakery.shelf_sour.release();
					continue;
				} catch (Exception e) {
					System.out.println("Error: Customer malfunctioned.");
				}
			}
			if (shoppingCart.get(i) == BreadType.WONDER) {
				try {
					bakery.shelf_wond.acquire();
					System.out.println("Customer " + hashCode() + " is shopping for " + shopTime + " miliseconds, at wonder shelf.");
					bakery.takeBread(shoppingCart.get(i));
					Thread.sleep(shopTime);
					System.out.println("Customer " + hashCode() + " finished at wonder shelf.");
					bakery.shelf_wond.release();
					continue;
				} catch (Exception e) {
					System.out.println("Error: Customer malfunctioned.");
				}
			}
		}
		// Check out
		try {
			bakery.cashiers.acquire();
			System.out.println("Customer " + hashCode() + " is at check out for " + checkoutTime + " miliseconds.");
			bakery.sales_mutex.acquire();
			bakery.addSales(getItemsValue());
			bakery.sales_mutex.release();
			Thread.sleep(checkoutTime);
			System.out.println("Customer " + hashCode() + " finished check out and is now leaving.");
			bakery.cashiers.release();
			
		} catch (Exception e) {
			System.out.println("Error: Customer malfunctioned.");
		}


	}

	/**
	 * Return a string representation of the customer
	 */
	public String toString() {
		return "Customer " + hashCode() + ": shoppingCart=" + Arrays.toString(shoppingCart.toArray()) + ", shopTime=" + shopTime + ", checkoutTime=" + checkoutTime;
	}

	/**
	 * Add a bread item to the customer's shopping cart
	 */
	private boolean addItem(BreadType bread) {
		// do not allow more than 3 items, chooseItems() does not call more than 3 times
		if (shoppingCart.size() >= 3) {
			return false;
		}
		shoppingCart.add(bread);
		return true;
	}

	/**
	 * Fill the customer's shopping cart with 1 to 3 random breads
	 */
	private void fillShoppingCart() {
		int itemCnt = 1 + rnd.nextInt(3);
		while (itemCnt > 0) {
			addItem(BreadType.values()[rnd.nextInt(BreadType.values().length)]);
			itemCnt--;
		}
	}

	/**
	 * Calculate the total value of the items in the customer's shopping cart
	 */
	private float getItemsValue() {
		float value = 0;
		for (BreadType bread : shoppingCart) {
			value += bread.getPrice();
		}
		return value;
	}
}