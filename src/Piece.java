import java.awt.Color;

public class Piece {

	int x;
	int y;
	Color color;
	pieceType type;
	
	public Piece(int x, int y, Color color, pieceType type)
	{
		this.color  = color;
		this.type = type;
		this.x = x;
		this.y = y;
	}
	
	//OVERRIDE: formatting instead of memory address
	public String toString()
	{
		StringBuilder sb = new StringBuilder ();
		sb.append("Piece: " + type +" (" + x + ", " + y +")");
		return sb.toString();
	}
	
	//isLegal: takes a piece of destination and determines if this piece is allowed to make that move
//	public boolean isLegal(Piece toPiece) {
//		
//	}
	
	

}
