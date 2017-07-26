import java.awt.Image;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
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

	public void addImage(String imageName) 
	{
		try 
		{
		    Image img = ImageIO.read(getClass().getResource(imageName));
		    this.setIcon(new ImageIcon(img));
		} 
		catch (Exception ex) 
		{
		    System.out.println(ex);
		}
		
	}

}
