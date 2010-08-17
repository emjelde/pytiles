<?xml version="1.0" encoding="UTF-8" ?>

<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:tiles="tiles/ns"
	extension-element-prefixes="tiles">

	<!-- Figure out what "type" of component this is from the value attribute. -->
	<xsl:template match="//put-attribute | //add-attribute">

		<xsl:variable name="type">
			<tiles:decideType>
				<xsl:value-of select="@value"/>
			</tiles:decideType>
		</xsl:variable>

		<xsl:variable name="elementName">
			<xsl:value-of select="local-name()"/>
		</xsl:variable>

		<xsl:element name="{$elementName}">
			<xsl:if test="@name != ''">
				<xsl:attribute name="name"><xsl:value-of select="@name"/></xsl:attribute>
			</xsl:if>
			<xsl:choose>
				<xsl:when test="@type != ''">
					<xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute>
				</xsl:when>
				<xsl:otherwise>
					<xsl:attribute name="type"><xsl:value-of select="$type"/></xsl:attribute>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:attribute name="value"><xsl:value-of select="@value"/></xsl:attribute>
		</xsl:element>

	</xsl:template>

	<!-- Recursively copy all nodes unchanged -->
	<xsl:template match="@* | node()">
		<xsl:copy>
			<xsl:apply-templates select="@* | node()"/>
		</xsl:copy>
	</xsl:template>

</xsl:stylesheet>
