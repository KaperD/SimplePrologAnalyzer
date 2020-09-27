package svgDraw;

import java.awt.*;

public class svgDraw {
    public svgDraw(int width, int height, Color backgroundColor) {
        backColor = String.format("rgb(%d,%d,%d)", backgroundColor.getRed(), backgroundColor.getGreen(), backgroundColor.getBlue());
        svgResult.append(String.format("<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"%d\" height=\"%d\" text-rendering=\"auto\" shape-rendering=\"auto\">\n", width, height));
        svgResult.append(String.format("<rect x=\"0\" y=\"0\" width=\"%d\" height=\"%d\" style=\"fill: %s; fill-opacity: 1.0\" />\n", width, height, backColor));
    }

    public void drawCircle(int xCenter, int yCenter, int radius) {
        svgResult.append(String.format("<circle cx=\"%d\" cy=\"%d\" r=\"%d\" stroke=\"black\" fill=\"%s\" stroke-width=\"1\"/>\n", xCenter, yCenter, radius, backColor));
    }

    public void drawCircle(int xCenter, int yCenter, int radius, Color fillColor) {
        svgResult.append(String.format("<circle cx=\"%d\" cy=\"%d\" r=\"%d\" fill=\"rgb(%d,%d,%d)\"/>\n", xCenter, yCenter, radius, fillColor.getRed(), fillColor.getGreen(), fillColor.getBlue()));
    }

    public void drawString(int x, int y, String str) {
        if (str.isEmpty()) return;
        int fontSize = Math.min(120 / str.length(), 40);
        svgResult.append(String.format("<text x=\"%d\" y=\"%d\" style=\"fill: black; fill-opacity: 1.0; text-anchor: middle; font-family: sans-serif; font-size: %dpx;\" dy = \".3em\">", x, y, fontSize));
        svgResult.append(str);
        svgResult.append("</text>\n");
    }

    public void drawLine(int x1, int y1, int x2, int y2) {
        svgResult.append(String.format("<line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" stroke=\"black\"/>\n", x1, y1, x2, y2));
    }

    public String getSvgResult() {
        svgResult.append("</svg>");
        return svgResult.toString();
    }

    private final StringBuilder svgResult = new StringBuilder();
    private String backColor;
}
