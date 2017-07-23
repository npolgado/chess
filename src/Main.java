import java.awt.Color;
import java.util.ArrayList;


public class Main {
	public static ArrayList<Piece> board = new ArrayList<>();	
	
	public static void main(String[] args) {
		Board b = new Board();
		b.setDefaultBoard(board);
		b.drawBoard(board);
	}
	
}
