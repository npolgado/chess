import java.awt.Color;
import java.util.ArrayList;

public class Piece {
	
	int index;
	int x;
	int y;
	Color color;
	pieceType type;
	
	public Piece(int x, int y, Color color, pieceType type, int index)
	{
		this.color  = color;
		this.type = type;
		this.x = x;
		this.y = y;
		this.index = index;
	}
	
	//OVERRIDE: formatting instead of memory address
	public String toString()
	{
		StringBuilder sb = new StringBuilder ();
		sb.append(this.index);
		return sb.toString();
	}
	
	//isLegal: takes a piece of destination and determines if this piece is allowed to make that move
	public boolean isLegal(Piece that) {
		switch (this.type) {
		case KNIGHT:
			return this.KnightLegal(that);
		case KING: 
			return this.KingLegal(that);
		case BISHOP:
			//return this.BishopLegal(that);
			break;
		default:
			return false;
		}
		return false;
	}
	
//	private boolean BishopLegal(Piece that) {
//		if(Math.abs(that.x - this.x)/Math.abs(that.y - this.y) == 1)
//		{
//			if(this.color == that.color)
//			{
//				return false;
//			}else
//			{
//				return true;
//			}
//		}
//		return false;
//	}

	private boolean KnightLegal(Piece that)
	{
		if(Math.abs(that.x - this.x) == 1 && Math.abs(that.y - this.y) == 2)
		{
			if(this.color == that.color)
			{
				return false;
			}else
			{
				return true;
			}
		}
		else if(Math.abs(that.x - this.x) == 2 && Math.abs(that.y - this.y) == 1)
		{
			if(this.color == that.color)
			{
				return false;
			}else
			{
				return true;
			}
		}
		return false;
	}

	private boolean KingLegal(Piece that)
	{
		if(Math.abs(that.x - this.x) == 1 && Math.abs(that.y - this.y) == 1)
		{
			if(this.color == that.color)
			{
				return false;
			}else
			{
				return true;
			}
		}
		return false;
	}
	

}
