<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0"
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:tiles="tiles/ns"
   extension-element-prefixes="tiles">

   <!-- Figure out what "type" of component this is from the value attribute. -->
   <xsl:template match="//put-attribute | //add-attribute">
      <xsl:variable name="type">
         <xsl:choose>
            <xsl:when test="@value != ''">
               <tiles:decideType>
                  <xsl:value-of select="@value"/>
               </tiles:decideType>
            </xsl:when>
            <xsl:otherwise>
               <xsl:text>definition</xsl:text>
            </xsl:otherwise>
         </xsl:choose>

      </xsl:variable>
      <xsl:element name="{local-name()}">
         <xsl:attribute name="type"><xsl:value-of select="$type"/></xsl:attribute>
         <xsl:copy-of select="@* | node()"/>
      </xsl:element>
   </xsl:template>

   <!-- Recursively copy all nodes unchanged -->
   <xsl:template match="@* | node()">
      <xsl:copy>
         <xsl:apply-templates select="@* | node()"/>
      </xsl:copy>
   </xsl:template>

</xsl:stylesheet>
