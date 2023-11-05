#version 460

uniform sampler2D image;
uniform float time;
uniform sampler2D iChannel0;

// in vec2 fragCoord;
in vec2 fragTexture;

out vec4 out_color;

vec2 CRTCurveUV( vec2 uv )
{
    uv = uv * 2.0 - 1.0;
    vec2 offset = abs( uv.yx ) / vec2( 3.0, 3.0 );
    uv = uv + uv * offset * offset;
    uv = uv * 0.5 + 0.5;
    return uv;
}

void DrawVignette( inout vec3 color, vec2 uv )
{    
    float vignette = uv.x * uv.y * ( 1.0 - uv.x ) * ( 1.0 - uv.y );
    vignette = clamp( pow( 16.0 * vignette, 0.4 ), 0.0, 1.0 );
    color *= vignette;
}

void DrawScanline( inout vec3 color, vec2 uv )
{
    // uv = uv.yx;
    float scanline = clamp(0.7 + 0.3 * cos( 3.14 * ( uv.y + 0.010 * time ) * 240.0 * 1.0 ), 0.0, 1.0 );
    float grille = 0.9 + 0.1 * clamp( 1.5 * cos( 3.14 * uv.x * 640.0 ), 0.0, 1.0 );    
    color *= scanline * grille * 1.6;
}

void DrawBlur( inout vec3 color, vec2 uv )
{
    float Tao = 6.28318530718; // Pi*2
    // GAUSSIAN BLUR SETTINGS {{{
    float Directions = 16.0; // BLUR DIRECTIONS (Default 16.0 - More is better but slower)
    float Quality = 4.0; // BLUR QUALITY (Default 4.0 - More is better but slower)
    float Size = 0.003; // BLUR SIZE (Radius)
    // GAUSSIAN BLUR SETTINGS }}}

    vec2 Radius = vec2(Size,Size);
    
    vec4 newColor = vec4(color,1.0);
    // Blur calculations
    for( float d=0.0; d<Tao; d+=Tao/Directions)
    {
		for(float i=1.0/Quality; i<1.001; i+=1.0/Quality)
        {
			newColor += texture( iChannel0, uv + (vec2(cos(d),sin(d)) * Radius * i));	
        }
    }
    newColor /= Quality * Directions + 1.0;
    color = newColor.rgb;
}

void main() {
    ivec2 iResolution = textureSize(image, 0);

    vec3 color = texture(image, fragTexture).rgb;

    // CRT effects (curvature, vignette, scanlines and CRT grille)
    vec2 uv = gl_FragCoord.xy / iResolution.xy;
    DrawBlur( color, uv );
    vec2 crtUV = CRTCurveUV( uv );
    if ( crtUV.x < 0.0 || crtUV.x > 1.0 || crtUV.y < 0.0 || crtUV.y > 1.0 )
    {
        color = vec3( 0.0, 0.0, 0.0 );
    }
    DrawVignette( color, crtUV );
    DrawScanline( color, uv );

	out_color.rgb = color;
    out_color.a = 1.0;
}
