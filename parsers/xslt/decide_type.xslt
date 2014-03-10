<?xml version="1.0" encoding="UTF-8" ?>

<!--
 Copyright (C) 2014 - Evan Mjelde

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->

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
