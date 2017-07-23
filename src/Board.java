import java.awt.Color;
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;
import javax.swing.border.Border;

public class Board {

	private int WIDTH = 400;
	private int HEIGHT = 400;
	private int OFFSETHEIGHT = 25;
	JFrame frame;
	
	public Board() {
		frame = new JFrame ("Chess");
		frame.setSize(WIDTH, HEIGHT + OFFSETHEIGHT);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);
	}
	
    public void drawBoard(int[][] ar) {
    	int count = 0;
    	int secCount = 0;
    	for (int a = 0; a < ar.length; a++) {
			for (int z = 0; z < ar.length; z++) {
				JButton button = new JButton(Integer.toString(ar[z][a]));
				button.setBounds(new Rectangle( ((WIDTH/8)*z), ((HEIGHT/8)*a), WIDTH/8, HEIGHT/8) );
				button.setOpaque(true);
				button.setBorderPainted(false);
				button.addActionListener(new EndingListener ());
				
				if (secCount % 8 == 0)
				{
					count ++;
				}
				
				if (count % 2 == 0)
				{
					button.setBackground (new Color (172, 112, 61));
				}
				frame.add(button);
				count ++;
				secCount++;
			}
		}    
    	
    	//if ur reading this, stay woke lil fucker
    	JButton fuker = new JButton ();
    	frame.add(fuker);
    	frame.setVisible(true);
    	
	}

    private class EndingListener implements ActionListener
    {
		public void actionPerformed(ActionEvent e) {
			System.out.println(e.getActionCommand());
		}
    }
	
}
