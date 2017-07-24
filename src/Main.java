import java.awt.Color;
import java.util.ArrayList;


public class Main {
	public static ArrayList<Piece> board = new ArrayList<>();	
	
	public static void main(String[] args) {
		Piece pawn1 = new Piece(4, 1, Color.BLACK, pieceType.PAWN);
		Piece empty1 = new Piece(4, 2, Color.BLUE, pieceType.EMPTY);
		
		Board b = new Board();
		
		board = b.setDefaultBoard(board);
		board = b.move(pawn1, empty1, board);
	}
	
}
