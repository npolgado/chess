import javax.swing.JButton;

public class ButtonExtend extends JButton{
	
	private Piece piece;
	
	public ButtonExtend() {
		super();
		piece = null;
	}
	
	public ButtonExtend (String s)
	{
		super(s);
	}
	
	public void setPiece(Piece piece){
		this.piece = piece;
	}
	
	public Piece getPiece(){
		return this.piece;
	}

}
