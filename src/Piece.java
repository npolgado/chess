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
	
	

}
