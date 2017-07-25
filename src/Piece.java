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
	
	//isLegal: takes a piece of destination and determines if this piece is allowed to make that move
	public boolean isLegal(Piece that, ArrayList<Piece> b) {
		switch (this.type) {
		case KNIGHT:
			return this.KnightLegal(that);
		case KING: 
			return this.KingLegal(that);
		case ROOK:
			return this.RookLegal(that, b);
		default:
			return false;
		}
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
		if(Math.abs(that.x - this.x) <= 1 && Math.abs(that.y - this.y) <= 1)
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

	private boolean RookLegal(Piece that, ArrayList<Piece> brd)
	{
		int a, b;
		Piece p = this;
		
		if((that.x - this.x) == 0)
		{
			if((that.y - this.y) < 0) //straight down
			{
				a = 0;
				b = -1;
			}else if (that.y - this.y > 0) //straight up
			{
				a = 0;
				b = 1;
			}
			else
			{
				return false;
			}
		}	
		else if((that.y - this.y) == 0)
		{
			if((that.x - this.x) < 0) //left
			{
				a = -1;
				b = 0;
			}else //right
			{
				a = 1;
				b = 0;
			}
		}else{
			return false;
		}
		
		for (int i = 0; i < brd.size(); i++)
		{
			if(p.equals(that)){
				return p.color != that.color;
			}
			if (brd.get(i).x == this.x + a && brd.get(i).y == this.y + b)
			{
				if(brd.get(i).type != pieceType.EMPTY){
					return false;
				}
				p = brd.get(i);
			}
		}
		return p.RookLegal(that, brd);
	}
	
	
	
	/* OVERRIDE: prints out the index in array (which is converted to an 
	 * int later to find the corresponding Piece) instead of memory address
	 */
	   
	public String toString()
	{
		StringBuilder sb = new StringBuilder ();
		sb.append(this.index);
		return sb.toString();
	}
	
	/* Overrides the equals method so we can compare temporary objects to the 
	 * original object in the array
	 */
	public boolean equals (Piece comparable)
	{
		return (this.color == comparable.color &&
				this.index == comparable.index &&
				this.type == comparable.type &&
				this.x == comparable.x &&
				this.y == comparable.y);
	}
	

}
